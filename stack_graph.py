#!/Library/Frameworks/Python.framework/Versions/Current/bin//python
def frange(start, stop, step):
	list = []
	while start < stop:
		list.append(start)
		start+=step
	return(list)
	
def grab_args(args):
	for i in xrange(len(args), 0, -1):
		print(args[i-1])
		if 'nx' in args[i-1]:
			nx = args.pop(i-1)
	
	nx = nx.split('=')[-1]
	nx = int(nx)
	return(nx, args)
	
def plot_stack(data, outfname=None):
	import matplotlib as mpl
	import matplotlib.pyplot as plt
	import matplotlib.figure as fig
	import matplotlib.image as mpimg
	from mpl_toolkits.axes_grid1 import ImageGrid
	import sys_to_si as s2s
	
	#print("sending to file: {}".format(outfname))

	fig1 = plt.gcf()
	fig1.clf()
	
	fig1.set_size_inches(40,40) #increase to improve quality
	nx = data[0] #unpack data
	pic_list = data[1] #unpack data
	ny = int(np.ceil(float(len(pic_list))/float(nx)))
	dx = 1.0/float(nx)
	dy = 1.0/float(ny)
	print(nx, ny, len(pic_list))
	img_list = [mpimg.imread(picture) for picture in pic_list] #make a list of image objects
	pic_shape = img_list[0].shape
	default = np.zeros(img_list[0].shape) #create a default picture, should be all black
	
	#fig1.subplots_adjust(left=0.0, bottom=0.0, right=1.0, top=1.0, wspace=0.0, hspace=0.0)
	fig1.set_frameon(False)
	grid = ImageGrid(fig1, 111, # similar to subplot(111)
                nrows_ncols = (ny, nx), # creates ny by nx grid of axes
                axes_pad=0.0, # pad between axes in inch.
                add_all=True,
                aspect = True
                )

	for i in range(nx*ny):
		if (i >= len(img_list)):
			grid[i].imshow(default, origin='upper')
		else:
			#have to change this sometimes if pics are upside-down
			grid[i].imshow(img_list[i], origin='upper')
		xmin, xmax, ymax, ymin = grid[i].axes.axis()
		xmin+=0.5
		xmax+=0.5
		ymin=np.floor(ymin+0.5)
		ymax=np.floor(ymax+0.5)
		if (ymin > ymax):
			temp = ymax
			ymax = ymin
			ymin = temp
		xmid = (xmin+xmax)/2.0
		if (i < len(img_list)):
			xmin = xmid - img_list[i].shape[0]/2.0
			xmax = xmid + img_list[i].shape[0]/2.0
		else:
			xmin = xmid - default.shape[0]/2.0
			xmax = xmid + default.shape[0]/2.0
		
		#grid[i].axes.axis((xmin, xmax, ymax,ymin)) #set the axes limits
		"""
		#grid[i].axes.axis((0, img_list[i].shape[0], img_list[i].shape[1], 0))
		grid[i].axes.invert_yaxis()
		grid[i].xaxis.set_ticks(frange(xmin+(xmax-xmin)/10, xmax, (xmax-xmin)/5)) #set where the ticks should be drawn
		grid[i].yaxis.set_ticks(frange(ymin+(ymax-ymin)/10, ymax, (ymax-ymin)/5))
		grid[i].xaxis.set_ticklabels(range(-4,7,2)) #set the values that should be drawn for the ticks
		grid[i].yaxis.set_ticklabels(range(-4,7,2))
		#grid[i].xaxis.set_label_text('AU') #set the axes lables
		grid[i].xaxis.set_label_position('bottom')
		#grid[i].yaxis.set_label_text('AU')
		grid[i].yaxis.set_label_position('left')
		"""
		#the next two commands stop axis things appearing
		grid[i].xaxis.set_tick_params(bottom='off', top='off', left='off', right='off',
			labelbottom='off', labeltop='off', labelleft='off', labelright='off')
		grid[i].yaxis.set_tick_params(bottom='off', top='off', left='off', right='off',
			labelbottom='off', labeltop='off', labelleft='off', labelright='off')
		
	#plt.show()
	#sys.exit()
	if outfname==None:
		plt.show()
	else:
		plt.savefig(outfname, bbox_inches="tight")

if __name__=='__main__':
	import sys, os
	from readss import unpackxdr_head
	import sys_to_si as s2s
	import numpy as np
	
	usage = '''
	"bin_graph.py" Creates graphs of the "ss.dust" files outputted by PKDGRAV's 
	rubble planetesimals collision model.
	bin_graph.py [graph_files] nx=[x_val] [output_folder]
	
	[graph_files] = a list of "graph.png" files to stack
	[output_file] = a file to put the stacked graphs in graph in.
	[x_val] = number of graphs to put in the x direction, will be in order of [graph_files]
	'''
	
	if (len(sys.argv) == 1) or (sys.argv[1]=='-h') or (sys.argv[1]=='--help'):
		print(usage)
		sys.exit(0)
	'''
	if len(sys.argv)>2:
		outpath = sys.argv[-1]
		max = -1
	else: 
		outpath = None
		max = 2
	
	if outpath=='None' or outpath=='none' or outpath=='NONE':
		outpath = None
	
	if outpath != None:
		outname = os.path.join(outpath,sys.argv[-1]+'.png')
	else: outname = None
	'''
	if len(sys.argv)>2:
		outname = sys.argv[-1]
	else: 
		outname = None
	#print("sending to file: {}".format(outname))
	data = grab_args(sys.argv[1:-1])
	plot_stack(data, outfname=outname) #use all the files at once
