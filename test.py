#!/Library/Frameworks/Python.framework/Versions/Current/bin//python

def remove_overlaps(data):
	'''
	This function should find overlapping particles and remove them
	or move them as user sees fit.
	put particles in cells, if neighbouring cells occupied test for overlaps
	'''
	import numpy as np
	pdata=data[0]
	dx,dy,dz = 0.001,0.001, 0.001
	min_x = min([r[2][0] for r in pdata])
	max_x = max([r[2][0] for r in pdata])
	min_y = min([r[2][1] for r in pdata])
	max_y = max([r[2][1] for r in pdata])
	min_z = min([r[2][2] for r in pdata])
	max_z = max([r[2][2] for r in pdata])
	min_max = ((min_x, max_x, dx), (min_y,max_y, dy), (min_z, max_z, dz))
	av_rad = sum([x[1] for x in pdata])/data[2]
	av_vol = (max_x-min_x)*(max_y-min_y)*(max_z-min_z)/data[2]
	#print(min_max, av_rad, av_vol)
	#print(np.ceil([(m[1]-m[0])/av_vol for m in min_max]))
	
	space_array = np.zeros(np.ceil([(m[1]-m[0])/m[2] for m in min_max]))
	print(space_array.shape)
	
	def sa_r(x,y,z):
		bin_x = np.floor((x-min_x)/dx)
		bin_y = np.floor((y-min_y)/dy)
		bin_z = np.floor((z-min_z)/dz)
		return(bin_x, bin_y, bin_z)
	
	for x in xrange(0, space_array.shape[0]):
		for y in xrange(0, space_array.shape[1]):
			for z in xrange(0, space_array.shape[2]):
				space_array[x][y][z] = []
	print('space_array initialised...')
	for particle in pdata:
		x,y,z = sa_r(*particle[2])
		space_array[x][y][z].append(particle[6])
	
	print('space_array populated...')
	for x in space_array:
		for y in x:
			for z in y:
				if len(z)>1: print('Possible collision between',z)


def hill_rad(M_p, M_s, a):
	import math
	return math.pow((M_p/(3*M_s)), 1.0/3.0)*a

def in_3hillsph(pdata1, pdata2):
	import math
	dr = [r1 - r2 for r1,r2 in zip(pdata1[2], pdata2[2])]
	if math.sqrt(sum([r*r for r in dr])) < 3*hill_rad(pdata2[0], 1, math.sqrt(sum([r*r for r in pdata2[2]]))):
		return(True)
	else: return(False)
def sculpt_sphere(data):
	'''
	This function should sculpt a sphere of user selected size around 
	a specific particle (made for removing 3 hill-sphere's of material
	around a jupiter mass particle)
	'''
	special = []
	for pdata in data[0]:
		if is_planet(pdata[5]):
			special.append(pdata)
			
	del_list=[]
	for pdata in data[0]:
		if is_planet(pdata[5]): continue
		for planet in special:
			if in_3hillsph(pdata, planet):
				del_list.append(pdata)
		
	return(del_list)
	
def is_planet(colour):
	#5,2,11,6,7
	if colour==5 or colour==2 or colour==11 or colour==6 or colour==7:
		return(True)
	else: return(False)
	
if __name__=='__main__':
	"""
	This is just to verify initial conditions and remove 
	anything overlapping/unwanted or perform some other 
	feat of initial condition poking
	"""
	
	from readss import unpackxdr, packxdr
	import sys, os
	
	del_list = []
	data = []
	ssfile = sys.argv[1]
	data  = unpackxdr(ssfile)
	#data = remove_overlaps(data)
	del_list = sculpt_sphere(data)
	print([x[6] for x in del_list])
	packxdr(sys.argv[2], data ,[x[6] for x in del_list])
	