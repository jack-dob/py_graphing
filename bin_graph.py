#!/Library/Frameworks/Python.framework/Versions/Current/bin//python

def make_pic(data_chunk, db_inner = 0.9, db_outer= 3.9, n_db = 15, x_min=-5, x_max=5, n=500):
	
	dx = float((x_max-x_min))/float(n)
	pic_array = np.zeros((n, n))
	x = 0
	while x < n:
		y=0
		while y < n:
			
			x_pos = float(x_min)+float(x)*dx
			y_pos = float(x_min)+float(y)*dx
			r = np.sqrt(x_pos*x_pos + y_pos*y_pos)
			db = which_db(r, db_inner, db_outer, n_db)
			sys.stdout.write('making map, x: %d, y: %d, db: %d, x_pos: %g y_pos: %g r: %g, dust: %g         \r'%(x, y, db, x_pos, y_pos, r, data_chunk[db][1]))
			pic_array[x][y] = data_chunk[db][1]
			y+=1
		x+=1
	return(pic_array)

def which_db(r, db_inner, db_outer, n_db):
	dr = (db_outer - db_inner)/n_db
	if (r >= db_outer) | (r <= db_inner):
		return(-1) #trash bin
	bin = np.floor((r - db_inner)/dr)
	return(int(bin))


def unpackdust(file):
	f = open(file, 'r')
	data = []
	for aline in f:
		bline = aline.split()
		#print(bline)
		datum = []
		if(bline[0]=='Trash'):
			datum.append(-1)
		else:
			datum.append(int(bline[0]))
		datum += map(float, bline[1:])
		data.append(datum)
	return(data)
	
def sumto(num, list):
	sum = 0.0
	if num > len(list):
		num = len(list)
	for i in xrange(num):
		sum+=list[i]
	return(sum)
	
def plot_dust(data_chunk, outfname=None):
	import matplotlib as mpl
	import matplotlib.pyplot as plt
	import matplotlib.figure as fig
	import sys_to_si as s2s
	
	'''
	data_chunk = [data, data2, data3...]
	data = [bin, dust_mass, %from bin 1, %from bin 2, %from bin 3...]
	'''
	fig.Figure.clear(plt.gcf())
	time = data_chunk[0]
	data_chunk = data_chunk[1]
	N_groups = len(data_chunk)
	N_origins = len(data_chunk[0]) - 2
	bin_norms = [data[1] for data in data_chunk]
	bin_origins = [data[2:] for data in data_chunk]
	#sys.exit() #for debugging
	pic_array = make_pic(data_chunk)
	pic_shape = pic_array.shape
	the_cmap = mpl.cm.get_cmap('gist_heat') #Sets which colour map to use
	#the_cmap.set_over('b')
	im = plt.imshow(pic_array, cmap=the_cmap, origin='lower', zorder=0)
	#plt.colorbar(extend='max') # add colour bar
	#print(pic_array)
	im.set_interpolation('bilinear') 
	#plt.xticks(range(pic_shape[1]/10, pic_shape[1], pic_shape[1]/5),range(-4,7,2))
	#plt.yticks(range(pic_shape[0]/10, pic_shape[0], pic_shape[0]/5),range(-4,7,2))
	#plt.xlabel('Displacement (AU)')
	#plt.ylabel('Displacement (AU)')
	#plt.show()
	
	if outfname==None:
		plt.show()
	else:
		pic_name = outfname.split(os.sep)
		pic_name[-1] = pic_name[-1].split('.')
		pic_name[-1][0] +='map'
		pic_name[-1] = '_'.join(pic_name[-1][:-1])
		pic_name[-1] += '.png'
		pic_name = os.sep.join(pic_name)
		print('\n'+pic_name)
		plt.savefig(pic_name)
	
	fig.Figure.clear(plt.gcf())
	width = 0.5
	bin_abs = []
	for i in xrange(len(bin_norms)):
		abs = []
		for j in xrange(len(bin_origins[0])):
			abs.append(bin_origins[i][j]*bin_norms[i])
		bin_abs.append(abs)
		
	bar_pos = range(1, len(data_chunk))
	"""
	col = ['r','g','b','k','c','m','y', 'w', (0.5,0.5,0.5), (0.7,0.5,0.5), (0.5,0.7,0.5),
			(0.5,0.5,0.7), (0.7,0.5,0.7), (0.5,0.7,0.7), (0.7,0.7,0.5), (0.7,0.7,0.7)]
	"""
		
	#print(bin_abs)
	plots = []
	for i in xrange(len(bin_abs)):
		plots.append(plt.bar(bar_pos, bin_abs[i], width = width, bottom = sumto(i, bin_abs[i]),
					color = mpl.cm.spectral(float(i)*(1.0/float(len(bin_abs)))), log=False))

	plt.xlim(0, len(data_chunk)+0.2*len(data_chunk))
	plt.minorticks_on()
	plt.title('Dust mass in each dust bin\nT = {0:08.2f} (years)'.format(s2s.year(time)))
	plt.xlabel('Bin Number')
	plt.ylabel('Mass in Bin')
	plt.xticks([pos+width/2 for pos in bar_pos], range(1, len(bar_pos)+1) )
	plt.legend([plot[0] for plot in plots], range(1,len(bar_pos)+1) )
	
	if outfname==None:
		plt.show()
		return(0)
	else:
		plt.savefig(outfname)
		return(0)
		
if __name__=='__main__':
	import sys, os
	from readss import unpackxdr_head
	import sys_to_si as s2s
	import numpy as np
	
	usage = '''
	"bin_graph.py" Creates graphs of the "ss.dust" files outputted by PKDGRAV's 
	rubble planetesimals collision model.
	
	bin_graph.py [dust_files] [output_folder]
	
	[dust_files] = a list of "ss.dust" files to graph
	[output_folder] = a folder to put the graphs in, will be named according to timestamp?
	'''
	
	if (len(sys.argv) == 1) or (sys.argv[1]=='-h') or (sys.argv[1]=='--help'):
		print(usage)
		sys.exit(0)
	
	if len(sys.argv)>2:
		outpath = sys.argv[-1]
		max = -1
	else: 
		outpath = None
		max = 2
	
	if outpath=='None' or outpath=='none' or outpath=='NONE':
		outpath = None
	
	for arg in sys.argv[1:max]:
		data_chunk = unpackdust(arg)
		(plist, time, n_particles) = unpackxdr_head(arg.rstrip('.dust'))
		ident_string = 'ss.{0:06.5f}.dust'.format(s2s.year(time))
		if outpath != None:
			outname = os.path.join(outpath,ident_string+'.png')
		else: outname = None
		plot_dust((time, data_chunk), outfname=outname)