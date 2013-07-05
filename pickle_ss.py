#!/Library/Frameworks/Python.framework/Versions/Current/bin//python

def pickle_ss(args):
	from readss import unpackxdr
	import cPickle as cpk
	
	f = open(args[0], 'w') #open the file to store pickled data in
	print('Opened, destination file {0}'.format(args[0]))
	for ssfile in args[1:]:
		data_chunk = unpackxdr(ssfile) #read in ssdata from file
		cpk.dump(data_chunk, f, cpk.HIGHEST_PROTOCOL) #dump the data in the pickle file
		print('Data pickled...')
	f.close()
	print('All data pickled, closed file {0}'.format(args[0]))

if __name__=='__main__':
	import sys
	
	pickle_ss(sys.argv[1:])
	

