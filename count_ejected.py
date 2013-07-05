#!/Library/Frameworks/Python.framework/Versions/Current/bin//python


def num_ejected(data_chunk):
	from eVa_graph import inst_e
	"""
	This function should count the number of ejected particles
	"""
	#calculate escape velocity, v_esc^2 = (2GM/r)
	#G=1, M=1
	print("Counting ejected particles...")
	#print(len(data_chunk))
	num_eject = 0
	for pdata in data_chunk[0]:
		'''
		#print(pdata[2])
		r = math.sqrt(sum([pos*pos for pos in pdata[2]]))
		v_esc2 = 2/r
		v2 = sum([vel*vel for vel in pdata[3]])
		if v_esc2 < v2: num_eject+=1
		'''
		if inst_e(pdata[0], pdata[2], pdata[3])[0] <= 0: num_eject+=1
	return(num_eject)
	
def store_ejected(data_chunk, outfname=None):
	import sys_to_si as s2s
	import cPickle as cpk #use this as can store complete precision
	f=open(outfname,'a')#open file
	#dump data
	cpk.dump((s2s.year(data_chunk[1]), num_ejected(data_chunk)), f, cpk.HIGHEST_PROTOCOL)
	#close file
	f.close()
	print("Storing data point...")
	
def plot_ejected(infname, outfname=None):
	import cPickle as cpk #use this as can store complete precision
	import matplotlib.pyplot as plt
	
	if outfname==None:
		f = open(infname, 'r')
		outfname = infname
		
	f = open(infname, 'r')
	data = []
	while True:
		try: apoint = cpk.load(f)
		except EOFError: break
		data.append(apoint)
	data.sort()
	f.close()
	plt.plot([x[0] for x in data],[y[1] for y in data], 'b-')
	
	#plt.legend(loc=4)
	plt.title('Ejected Planetesimal Count')
	plt.xlabel('Time (Years)')
	plt.ylabel('Number of Ejected Planetesimals')
	if outfname==None:
		plt.savefig(infname)
	else:
		plt.savefig(outfname)
	



if __name__=='__main__':
	import matplotlib.pyplot as plt
	from readss import unpackxdr
	from unpickle_chunk import unpickle_chunk
	import sys, os
	
	if len(sys.argv)>2:
		outpath = sys.argv[-1]
	else: outpath = None
	
	
	alist = []
		
	if '.dat' in sys.argv[1]:
		for data_chunk in unpickle_chunk(sys.argv[1]):
			aproperty = num_ejected(data_chunk)
			alist.append((data_chunk[1], aproperty))
	else:
		for data_chunk in [unpackxdr(sys.argv[1])]:
			aproperty = num_ejected(data_chunk)
			alist.append((data_chunk[1], aproperty))
	
	alist.sort() #sorts by first number in tuple, time in this case
	plt.plot([x[0] for x in alist],[y[1] for y in alist]) #plot the data
	
	#plt.ticklabel_format(axis='y', scilimits=(-3,3))
	plt.title(TITLE)
	plt.xlabel(X_TITLE)
	plt.ylabel(Y_TITLE)
	
	
	if outpath==None: outname=None
	else: 
		ident_string = 'ejected_particles'
		outname = os.path.join(sys.argv[-1],ident_string+'.png')
	
	if outname==None:
		plt.show()
	else:
		plt.savefig(outname)
		