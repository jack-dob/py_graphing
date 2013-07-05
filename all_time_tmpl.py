#!/Library/Frameworks/Python.framework/Versions/Current/bin//python


def FUNCTION_NAME(data_chunk):
	"""
	This function should create a data point for each time step
	"""
	return(0)

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
			aproperty = FUNCTION_NAME(data_chunk)
			alist.append((data_chunk[1], aproperty))
	else:
		for data_chunk in [unpackxdr(sys.argv[1])]:
			aproperty = FUNCTION_NAME(data_chunk)
			alist.append((data_chunk[1], aproperty))
	
	plt.plot([x[0] for x in alist],[y[1] for y in alist]) #plot the data
	
	#plt.ticklabel_format(axis='y', scilimits=(-3,3))
	plt.title(TITLE)
	plt.xlabel(X_TITLE)
	plt.ylabel(Y_TITLE)
	
	
	if outpath==None: outname=None
	else: 
		ident_string = 'property_name'
		outname = os.path.join(sys.argv[-1],ident_string+'.png')
	
	if outname==None:
		plt.show()
	else:
		plt.savefig(outname)
		