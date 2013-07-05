#!/Library/Frameworks/Python.framework/Versions/Current/bin//python
def cross_prod(a, b):
	i = a[1]*b[2]-b[1]*a[2]
	j = b[0]*a[2]-a[0]*b[2]
	k = a[0]*b[1]-b[0]*a[1]
	return(i,j,k)

def dot_prod(a, b):
	i = a[0]*b[0]
	j = a[1]*b[1]
	k = a[2]*b[2]
	return(i+j+k)
	
def inst_V(mass, pos, vel):  
    from math import sqrt
    #remember m is in solar masses, pos in AU, speed in AU/(2PI*yr)
    h = cross_prod(pos,vel) #h_vec = pos_vec X vel_vec
    h2 = sum([hi*hi for hi in h])
    spd2 = sum([veli*veli for veli in vel])
    a = sqrt(sum([j*j for j in pos]))
    G = 1.0 #grav const =1 in the sim for less operations, M is in solar masses, so M=1
    sma = 1/(2/a-spd2/(G*(1+mass)))
    return(sma, sqrt(spd2))
    #return(a, sqrt(spd2))

def resonance(a, c1,c2):
	import math
	
	P = math.sqrt(a*a*a)
	P_res = (c1*P)/c2
	a_res = math.pow(P_res*P_res, 1.0/3.0)
	return(a_res)
	
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

	
def hill_rad(M_p, M_s, a):
	import math
	return math.pow((M_p/(3*M_s)), 1.0/3.0)*a

def plot_RV(data_chunk, outfname=None):
	import sys_to_si as s2s
	import matplotlib.pyplot as plt
	import matplotlib.figure as fig
	
	(pdata, systime, particle_num) = data_chunk
	fig.Figure.clear(plt.gcf())
	print('Plotting data...')
	#pdata format = mass, radius, pos(xyz), vel(xyz), spin(xyz), colour, original_identifier
	#print([stuff[2] for stuff in pdata[:5]])
	
	es = [inst_V(e[0], e[2],e[3]) for e in pdata] #get data for plot
	#print('HERE', es[:2])
	#print(sum([veli*veli for veli in pdata[0][3]]))
	#print(sum([veli*veli for veli in pdata[1][3]]))
	
	plt.plot([e[0] for e in es[1:]],[e[1] for e in es[1:]], 'r.',zorder=0, ms=0.2) 
	#plot the data, 'zorder=0' makes sure that it is drawn first and everything else is on top of it
	
	#Draw vertical lines at resonances and add labels
	plt.axvline(x=resonance(es[0][0],1,2), ymin=0, ymax=1, c='g', ls='--', label='Resonances')
	plt.text(resonance(es[0][0],1,2), 0.8, '1:2', color='k', rotation=90, ha='center')
	
	plt.axvline(x=resonance(es[0][0],1,3), ymin=0, ymax=1, c='g', ls='--', label='_nolegend_')
	plt.text(resonance(es[0][0],1,3), 0.8, '1:3', color='k', rotation=90, ha='center')
	
	plt.axvline(x=resonance(es[0][0],2,3), ymin=0, ymax=1, c='g', ls='--', label='_nolegend_')
	plt.text(resonance(es[0][0],2,3), 0.8, '2:3', color='k', rotation=90, ha='center')
	
	plt.axvline(x=resonance(es[0][0],2,1), ymin=0, ymax=1, c='g', ls='--', label='_nolegend_')
	plt.text(resonance(es[0][0],2,1), 0.8, '2:1', color='k', rotation=90, ha='center')
	
	plt.axvline(x=resonance(es[0][0],3,2), ymin=0, ymax=1, c='g', ls='--', label='_nolegend_')
	plt.text(resonance(es[0][0],3,2), 0.8, '3:2', color='k', rotation=90, ha='center')
	
	
	#plot planet data with error bars for hill radii
	plt.errorbar(x=es[0][0], y=es[0][1], yerr=None, xerr=5*hill_rad(pdata[0][0],1,es[0][0]), 
					elinewidth=None, barsabove=True, marker='o',
					ms=30*hill_rad(pdata[0][0],1,es[0][0])/hill_rad(10E-3,1,es[0][0]),
					mec='b', mfc='None', mew=1)

	plt.axis([0,5,-0.05,1])
	
	#put in lables and titles etc
	plt.minorticks_on()
	plt.title('Velosity Magnitude vs Semi-major Axis:\nT = {0:08.2f} (years), N = {1:07}'.format(s2s.year(systime), particle_num))
	plt.xlabel('Semi-major Axis  (AU)')
	plt.ylabel('Velocity (2PI AU per Year)')
	plt.legend()
	
	if outfname==None:
		plt.show()
		return(0)
	else:
		plt.savefig(outfname)
		return(0)

if __name__=='__main__':
	import matplotlib.pyplot as plt
	from readss import unpackxdr
	from unpickle_chunk import unpickle_chunk
	import sys, os, math
	'''
	All passed arguments except the last one are assumed to be data files.
	therefore wildcards are placed before the destination folder.
	e.g.
		eVa_graph.py thefiles* ./destination_folder/
	'''
	if len(sys.argv)>2:
		outpath = sys.argv[-1]
		max = -1
	else: 
		outpath = None
		max = 2
	
	if '.dat' in sys.argv[1]:
		for data_chunk in unpickle_chunk(sys.argv[1]):
			ident_string = 'ss.{0:05.0f}'.format(data_chunk[1])
			outname = os.path.join(outpath,ident_string+'.png')
			plot_RV(data_chunk, outfname=outname)
	else:
		for arg in sys.argv[1:max]:
			data_chunk = unpackxdr(arg)
			ident_string = 'ss.{0:05.0f}'.format(data_chunk[1])
			if outpath != None:
				outname = os.path.join(outpath,ident_string+'.png')
			else: outname = None
			plot_RV(data_chunk, outfname=outname)


