#!/Library/Frameworks/Python.framework/Versions/Current/bin//python

def frange(start, stop, step):
	precisionlist = []
	for num in (float(start),float(stop),float(step)):
		i=0
		while not num.is_integer():
			num*=10
			i+=1
		precisionlist.append(i)
	precision = max(precisionlist)+1
	while start<stop:
		yield(start)
		start+=step
		start = round(start,precision)
	#print(list,len(list))
	
def bin_func(x_bins, y_bins, dx, dy, xmin, ymin ,data_chunk):
	import numpy as np
	"""
	This bins the data into bins of the size dx in x direction, dy in y direction.
	The binning is weighted by the mass of the particle so we get surface density.
	
	The jupiter is ignored as it is so much larger than everything else it screws
	up the colour range.-->Fixed now
	"""
	#pos = [i[2] for i in data_chunk[0]]
	
	
	au2_earthM=dx*dy*3E-6 #to put stuff in units of earth masses per square AU
	
	bin_array=np.zeros((y_bins,x_bins)) #create the array with zeros initially
	# remember, uses y,x format, index from 0->(n-1) [hence -1 in whichx/y]
	x_bins-=1
	y_bins-=1
	print('Binning data...')
	
	#ignore jupiter (here the 1st particle, could also select by colour number)
	for particle in data_chunk[0]:
		#work out where to put each planetesimal
		whichx = int(np.floor((particle[2][0]-xmin)/dx)-1)
		whichy = int(np.floor((particle[2][1]-ymin)/dy)-1)
		if (0>whichx)|(0>whichy)|(x_bins<whichx)|(y_bins<whichy): 
			#if particle is outside range covered by view, ignore it
			continue
		#otherwise, put it in the array at the correct position
		bin_array[whichy][whichx]+=(particle[0]/(au2_earthM))
	print('Data binned...')
	return bin_array

def r2(dat):
	return sum(r*r for r in dat[2])

def density_graph(data, dx=0.05, dy=0.05, xmax=5, xmin=-5, ymax=5, ymin=-5,
				colourmap='gnuplot', c_bar_lims=(000000,800000), 
				autoda=False, outfname=None, type=[]):
	import sys_to_si as s2s
	import matplotlib.pyplot as plt
	import numpy as np
	import matplotlib as mpl
	import matplotlib.figure as fig
	import math
	
	fig.Figure.clear(plt.gcf())
	

	print(data.shape)
	z_shape = data.shape
	print('Plotting image...')
	
	if 'differential' in type:
		dx = 0.0125
		dy = 0.0125
		dr = math.sqrt(dx*dx + dy*dy)
		ref = np.copy(data)
		#data = np.zeros(z_shape)
		if data is ref:
			print('BOO')
		if data is not ref:
			print('YAY')
		mid = (math.floor(z_shape[0]/2.0), math.floor(z_shape[1])/2.0)
		for i in xrange(1,z_shape[0]):
			for j in xrange(1,z_shape[1]):
				x = i-mid[0]
				y = j-mid[1]
				r = math.sqrt(x*x+y*y)
				try:
					dr_x = float(x)/float(r)
					dr_y = float(y)/float(r)
				except ZeroDivisionError:
					dr_x = 01.0
					dr_y = 01.0
				grad_x = (ref[i][j]-ref[i-1][j])/dx
				grad_y = (ref[i][j]-ref[i][j-1])/dy
				DD = abs(grad_x/dr_x +grad_y/dr_y)
				if dr_x ==0:
					DD = abs((grad_x/(dr_x+1) + grad_x/(dr_x-1))/2 +grad_y/dr_y)
				if dr_y ==0:
					DD = abs((grad_y/(dr_y+1) + grad_y/(dr_y-1))/2 +grad_x/dr_x)
				if (dr_y==0)and(dr_x==0):
					DD = abs((grad_y/(dr_y+1) + grad_y/(dr_y-1))/2 +(grad_x/(dr_x+1) + grad_x/(dr_x-1))/2)
				data[i][j] = DD
				#print(x, y, r, DD)
				
	
	#plt.hot()
	the_cmap = mpl.cm.get_cmap(colourmap) #Sets which colour map to use
	#the_cmap.set_over('b')
	im = plt.imshow(data, cmap=the_cmap,
					origin='lower', zorder=0) 
					# put the image on plot, using 'gnuplot' colour map
					# origin at bottom left, draw this first
					# list of colourmaps: http://matplotlib.sourceforge.net/examples/pylab_examples/show_colormaps.html
					
	plt.colorbar(extend='max') # add colour bar
	#set interpolation level
	#im.set_interpolation('nearest')
	#im.set_interpolation('bicubic')
	im.set_interpolation('bilinear') 
	
	#im.set_clim(*c_bar_lims) # Sets the lower and upper limits of the colour bar.
	#plt.gca().invert_yaxis()
	plt.xticks(range(z_shape[1]/10, z_shape[1], z_shape[1]/5),range(-4,7,2))
	plt.yticks(range(z_shape[0]/10, z_shape[0], z_shape[0]/5),range(-4,7,2))
	plt.xlabel('Displacement (AU)')
	plt.ylabel('Displacement (AU)')
	#title2='Surface density in M$_\oplus/$AU$^2$\n$T$ = %08.2f (yrs),  $N$ = %07d, $d_{area}$=%04.2g (AU$^2$)' %(s2s.year(data_chunk[1]), data_chunk[2], dx*dy)
	title2 = 'Test graph 1'
	plt.title(title2)
	print('Saving figure...')
	
	if outfname==None:
		plt.show()
		return(0)
	else:
		plt.savefig(outfname)
		return(0)

def read_in_grids(args):
	import numpy as np
	count = len(args)
	f = open(args[0])
	y = 0
	for aline in f:
		x = len((aline.strip()).split(' '))
		y+=1
	f.close()
	print((count, y, x))
	data_cube = np.zeros((count, y, x))
	i=0
	for arg in args:
		f = open(arg)
		j=0
		for aline in f:
			k=0
			for number in map(float,(aline.strip()).split(' ')):
				data_cube[i][j][k] = number
				k+=1
			j+=1
		f.close()
		i+=1
	
	return(data_cube) 
if __name__=='__main__':
	import sys, os
	from unpickle_chunk import unpickle_chunk
	from readss import unpackxdr
	import numpy as np
	
	#print(plt.cm.datad.keys())
	#sys.exit(0)
	if len(sys.argv)>2:
		outpath = sys.argv[-1]
	else: outpath = None
	
	data_cube = read_in_grids(sys.argv[1:])
	
	for data_square in data_cube:
		density_graph(data_square, type = [])#'differential'])