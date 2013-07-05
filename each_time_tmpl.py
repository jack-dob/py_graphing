#!/Library/Frameworks/Python.framework/Versions/Current/bin//python


def FUNCTION_NAME(data_chunk):
	"""
	This function should create a graph for each time step
	"""
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
				FUNCTION_NAME(data_chunk)
			else:
				outname = os.path.join(sys.argv[-1],ident_string+'.png')
				FUNCTION_NAME(data_chunk, outfname=outname)
	else:
		for data_chunk in [unpackxdr(sys.argv[1])]:
			ident_string = 'ss.{0:05.0f}'.format(data_chunk[1])
			if outpath==None:
				FUNCTION_NAME(data_chunk)
			else:
				outname = os.path.join(sys.argv[-1],ident_string+'.png')
				FUNCTION_NAME(data_chunk, outfname=outname)
		