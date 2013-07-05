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

def surf_density(data_chunk, dx=0.1, dy=0.1, xmax=11, xmin=-11, ymax=11, ymin=-11,
				colourmap='gnuplot', c_bar_lims=(0,0.2), autoda=False, 
				outfname=None):# change these as needed
	import sys_to_si as s2s
	import matplotlib.pyplot as plt
	import numpy as np
	import matplotlib as mpl
	import matplotlib.figure as fig
	"""
	This function creates a surface density plot of a solar system simulation
	Arguments:
		data_chunk	=		[tuple] (pdata, time, n_particles) from either
							'unpackxdr()' on readss or 'unpickle_chunk()'.
		dx, dy 		=		step in x, y dimension used for resolution, also
							sets the lower limit for autoda. [number]
		xmax, ymax	=		The upper x, y limits of the plot [number]
		xmin, ymin	=		The lower x, y limits of the plot [number]
		colourmap	=		The name of the colour map to use, see
							http://matplotlib.sourceforge.net/examples/pylab_examples/show_colormaps.html
							for a list of colourmaps.
		c_bar_lims	=		The bottom and top limits of the colourbar, make sure
							objects are visible in the range set.
		autoda		=		This flag sets weather to auromatically determine
							the dx, dy steps using the dx, dy values in the
							arguments as lower limits. [Bool]
	"""
	fig.Figure.clear(plt.gcf())
	
	inview=[dat[2] for dat in data_chunk[0] if r2(dat)<(xmin*ymin)]
	x_range=max([x[0] for x in inview])-min([x[0] for x in inview])
	y_range=max([x[1] for x in inview])-min([x[1] for x in inview])
	n_particles = len(inview) #this many particles (total)
	area=3.142*(y_range)*(x_range) #this much view space
	#average distance between them, will be overestimate 
	#if some particles not in view area
	smallest_dxy = np.sqrt(area/n_particles)
	#print(smallest_dxy)
	if autoda:
		print('Automatically determining optimum binsize...')
		if smallest_dxy>((dx+dy)/2):
			if smallest_dxy>10*((dx+dy)/2):
				print('Using 10* dx, dy as upper limits')
				dx*=10
				dy*=10
			else:
				dx = smallest_dxy
				dy = smallest_dxy
		else:
			print('Using given dx, dy as lower limits...')
	elif dx*dy<(smallest_dxy*smallest_dxy):
		print('Warning: Resolution smaller than average inter-particle distance...')
		
	x_bins = int(np.floor((xmax-xmin)/dx))
	y_bins = int(np.floor((ymax-ymin)/dy))
	
	Zs = bin_func(x_bins, y_bins, dx, dy, xmin, ymin,data_chunk)
	#Zs contains the Z value for each grid position, calculated by func3()
	z_shape = Zs.shape
	print('Plotting image...')
	
	#plt.hot()
	the_cmap = mpl.cm.get_cmap(colourmap) #Sets which colour map to use
	#the_cmap.set_over('b')
	im = plt.imshow(Zs, cmap=the_cmap,
					origin='lower', zorder=0) 
					# put the image on plot, using 'gnuplot' colour map
					# origin at bottom left, draw this first
					# list of colourmaps: http://matplotlib.sourceforge.net/examples/pylab_examples/show_colormaps.html
					
	plt.colorbar(extend='max') # add colour bar
	#set interpolation level
	#im.set_interpolation('nearest')
	#im.set_interpolation('bicubic')
	im.set_interpolation('bilinear') 
	
	im.set_clim(*c_bar_lims) # Sets the lower and upper limits of the colour bar.
	#plt.gca().invert_yaxis()
	#plt.xticks(range(z_shape[1]/10, z_shape[1], z_shape[1]/5),range(-4,7,2))
	#plt.yticks(range(z_shape[0]/10, z_shape[0], z_shape[0]/5),range(-4,7,2))
	plt.xticks(range(z_shape[1]/22, z_shape[1], z_shape[1]/11),range(-10,11,2))
	plt.yticks(range(z_shape[0]/22, z_shape[0], z_shape[0]/11),range(-10,11,2))
	plt.xlabel('Displacement (AU)', fontsize=18)
	plt.ylabel('Displacement (AU)', fontsize=18)
	#title2='Surface density in M$_\oplus/$AU$^2$\n$T$ = %08.2f (yrs),  $N$ = %07d, $d_{area}$=%04.2g (AU$^2$)' %(s2s.year(data_chunk[1]), data_chunk[2], dx*dy)
	title2 = '$T$ = %08.2f (yrs)\n$N$ = %07d' %(s2s.year(data_chunk[1]), data_chunk[2])
	plt.title(title2, fontsize=24)
	plt.plot(int(np.floor((data_chunk[0][0][2][0]-xmin)/dx)-1),
			int(np.floor((data_chunk[0][0][2][1]-ymin)/dy)-1), 'go', ms=20,
			axes=plt.gca(), mfc='None', mec='g', mew=2) 
			# puts jupiter in correct place as a green circle
	print('Saving figure...')
	
	if outfname==None:
		plt.show()
		return(0)
	else:
		plt.savefig(outfname, bbox_inches="tight")
		return(0)

if __name__=='__main__':
	import sys, os
	from unpickle_chunk import unpickle_chunk
	from readss import unpackxdr
	
	#print(plt.cm.datad.keys())
	#sys.exit(0)
	if len(sys.argv)>2:
		outpath = sys.argv[-1]
	else: outpath = None
	
	if '.dat' in sys.argv[1]:
		for data_chunk in unpickle_chunk(sys.argv[1]):
			ident_string = 'ss.{0:05.0f}'.format(data_chunk[1])
			if outpath==None:
				surf_density(data_chunk)
			else:
				outname = os.path.join(sys.argv[-1],ident_string+'.png')
				surf_density(data_chunk, outfname=outname)
	else:
		for data_chunk in [unpackxdr(sys.argv[1])]:
			ident_string = 'ss.{0:05.0f}'.format(data_chunk[1])
			if outpath==None:
				surf_density(data_chunk)
			else:
				outname = os.path.join(sys.argv[-1],ident_string+'.png')
				surf_density(data_chunk, outfname=outname)
		
	