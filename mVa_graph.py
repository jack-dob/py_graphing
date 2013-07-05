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
	
def bin_func(dr, rmin, rmax ,data_chunk):
	import numpy as np
	"""
	This bins the data into bins of radius dr.
	The binning is weighted by the mass of the particle so we get surface density.
	
	The jupiter is ignored as it is so much larger than everything else it screws
	up the colour range.-->Fixed now
	"""
	#pos = [i[2] for i in data_chunk[0]]
	n_bins = (rmax-rmin)/dr
	
	bin_array=np.zeros((n_bins)) #create the array with zeros initially
	# remember, uses y,x format, index from 0->(n-1) [hence -1 in whichx/y]
	n_bins-=1
	print('Binning data...')
	earthmass = 3E-6
	#ignore jupiter (here the 1st particle, could also select by colour number)
	for particle in data_chunk[0][1:]:
		#work out where to put each planetesimal
		whichr = int(np.floor((sma(particle)-rmin)/dr)-1)
		if (0>whichr)|(n_bins<whichr)|(particle[5]!=3): 
			#if particle is outside range covered by view,
			#not on eliptical orbit, or not a planetesimal, ignore it
			continue
		#otherwise, add it's mass to the array at the correct position
		bin_array[whichr]+=(particle[0])/earthmass #put into earth masses
	print('Data binned...')
	return bin_array

def r2(dat):
	return sum(r*r for r in dat[2])

def v2(dat):
	return sum(v*v for v in dat[3])

def sma(dat):
	import numpy as np
	r = np.sqrt(r2(dat))
	spd2 = v2(dat)
	G=1
	mass = dat[0]
	#print(r, spd2, G, mass)
	return(1/(2/r-spd2/(G*(1+mass))))

def draw_resonances(obj, dr, reslist):
	from eVa_graph import resonance
	import numpy as np
	import matplotlib.pyplot as plt
	
	(xmin, xmax, ymin ,ymax) = plt.axis()
	#print(xmin, xmax, ymin ,ymax)
	#print(obj)
	a = sma(obj)
	
	i=0
	for res in reslist:
		if i==0: alabel='resonances'
		else: alabel='_nolegend_'
		if res == (1,1): lsstr = '-'
		else: lsstr='--'
		#print(res)
		xpos = (resonance(a,*res)-xmin)/dr
		plt.axvline(x=xpos, ymin=0, ymax=1, c='g', ls=lsstr, label=alabel)
		plt.text(xpos, 0.8*(ymax-ymin), str(res[0])+':'+str(res[1]), color='k', rotation=90, ha='center')
		i+=1
		
def mVa_graph(data_chunk, dr=0.001, rmax=5, rmin=0, ymax=0.01, ymin=0, 
			outfname=None, FILL=True, BAR=True): #change as needed
	import sys_to_si as s2s
	import matplotlib.pyplot as plt
	import numpy as np
	import matplotlib as mpl
	import math
	
	mpl.figure.Figure.clear(plt.gcf())
	
	Zs = bin_func(dr, rmin, rmax, data_chunk)
	#Zs contains the Z value for each grid position, calculated by func3()
	z_shape = Zs.shape
	#print(z_shape)
	print('Plotting image...')
	if BAR:
		plt.bar(np.arange(0,z_shape[0]), Zs, width=1, bottom=0, color='red', edgecolor='red')
	else:
		plt.plot(Zs, 'r-')
	plt.axis([0, z_shape[0], ymin, ymax])
	plt.xticks(range(0, z_shape[0], z_shape[0]/5),range(0,6,1))
	#plt.ylim(0,0.01)
	draw_resonances(data_chunk[0][0],dr, [(1,1),(1,2),(2,3),(1,3),(2,1),(3,2)])

	xs = range(1,100)
	#plt.plot(xs,[max(Zs)/math.pow(y*float(5)/100, 0.5) for y in xs], 'b--')
	if FILL and not BAR:
		plt.gca().fill_between(np.arange(0,z_shape[0]),0, Zs, facecolor='red')
	
	plt.xlabel('Semi-major axis (AU)')
	plt.ylabel('Mass (M$_\oplus$)')
	#title2='Mass Evolution w.r.t Semi-Major Axis\n$T$ = %08.2f (yrs),  $N$ = %07d, $d_r$=%02g (AU)' %(s2s.year(data_chunk[1]), data_chunk[2], dr)
	title2 = '$T$ = %08.2f (yrs),  $N$ = %07d, $d_r$=%02g (AU)' %(s2s.year(data_chunk[1]), data_chunk[2], dr)
	plt.title(title2)
	plt.legend()
	print('Saving figure...')
	
	if outfname==None:
		plt.show()
		return(0)
	else:
		plt.savefig(outfname)
		return(0)

if __name__=='__main__':
	import sys, os
	from readss import unpackxdr
	from unpickle_chunk import unpickle_chunk
	
	#print(plt.cm.datad.keys())
	#sys.exit(0)
	if len(sys.argv)>2:
		outpath = sys.argv[-1]
	else: outpath = None
	
	if '.dat' in sys.argv[1]:
		for data_chunk in unpickle_chunk(sys.argv[1]):
			ident_string = 'ss.{0:05.0f}'.format(data_chunk[1])
			if outpath==None:
				mVa_graph(data_chunk)
			else:
				outname = os.path.join(sys.argv[-1],ident_string+'.png')
				mVa_graph(data_chunk, outfname=outname)
	else:
		for data_chunk in [unpackxdr(sys.argv[1])]:
			ident_string = 'ss.{0:05.0f}'.format(data_chunk[1])
			if outpath==None:
				mVa_graph(data_chunk)
			else:
				outname = os.path.join(sys.argv[-1],ident_string+'.png')
				mVa_graph(data_chunk, outfname=outname)
		
	