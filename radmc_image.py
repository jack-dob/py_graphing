#!/Library/Frameworks/Python.framework/Versions/Current/bin//python

AU=1.49597871E13 #cm per AU

def plot_arrays(arrays, outfname=None):
	import matplotlib.pyplot as plt
	import matplotlib.figure as fig
	
	F=plt.gcf()
	for array in arrays:
		im = plt.imshow(array, origin='lower')
		print(array.shape, type(im))
		plt.xticks(range(array.shape[0]/10, array.shape[0], array.shape[0]/5), range(-4,7,2))
		plt.yticks(range(array.shape[1]/10, array.shape[1], array.shape[1]/5), range(-4,7,2))
		#plt.xlabel('AU', fontsize=30)
		#plt.ylabel('AU', fontsize=30)
		#plt.tick_params(axis='both', which='major', labelsize=26)
		plt.colorbar(extend='max')
		plt.tick_params(bottom='off', top='off', left='off', right='off',
			labelbottom='off', labeltop='off', labelleft='off', labelright='off')
		plt.tick_params(bottom='off', top='off', left='off', right='off',
			labelbottom='off', labeltop='off', labelleft='off', labelright='off')
		dpi = F.get_dpi()
		F.set_size_inches(1100/dpi, 1100/dpi)
		if (outfname==None):
			plt.show()
		else:
			plt.savefig(outfname)#, bbox_inches='tight')
		

def plot_radmc_image(pic_files, outfname=None):
	import matplotlib.pyplot as plt
	import matplotlib.figure as fig
	import numpy as np
	
	pictures = []
	for pic in pic_files:
		f = open(pic, "r") #open the file
		iformat = int(f.readline()) #should always be 1
		print("iformat: {}".format(iformat))
		nx, ny = map(int, f.readline().split()) #pixels in x and y direction
		print("nx: {}, ny: {}".format(nx, ny))
		nlam = int(f.readline()) #number of wavelengths in file
		print("nlam: {}".format(nlam))
		psize_x, psize_y = map(float, f.readline().split()) #the size of pixels in cm
		print("psize_x: {}, psize_y: {}".format(psize_x/AU, psize_y/AU))
		lambdas = map(float, f.readline().split()) #list of wavelengths in the file
		print("lambdas: {}".format(lambdas))
		f.readline() #an empty line
		
		for k in xrange(0, nlam): #loop over number of images
			array = np.empty((nx, ny)) #create an empty array
			for j in xrange(0, ny):
				for i in xrange(0, ny):
					array[j][i] = np.float(f.readline()) #opposite way round to what I think
			pictures.append(array) #store picture in list
		f.close() #close the file
	plot_arrays(pictures, outfname)

if __name__=="__main__":
	import sys, os
	
	if len(sys.argv) >2:
		outfname = sys.argv[-1]
		args = sys.argv[1:-1]
	else:
		outfname=None
		args = sys.argv[1:]
	
	plot_radmc_image(args, outfname)
	