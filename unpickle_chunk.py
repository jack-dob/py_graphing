#!/Library/Frameworks/Python.framework/Versions/Current/bin//python

def unpickle_file(datfile):
	"""
	This chucks all the data into the memory at once, unlikely to be the
	best way of doing something, but use if needed.
	"""
	import cPickle as cpk
	
	f = open(datfile, 'r') #open the file to store pickled data in
	
	data = [] #create empty list for data
	while True:
		try: data.append(cpk.load(f))
		except EOFError:
			print('Unpickling finished, data loaded...')
			break
	f.close()
	return(data)
	
def unpickle_chunk(datfile):
	import cPickle as cpk
	"""
	This only loads one ss-file's worth of data at once, is alot more memory efficient
	than code above.
	Is written as a generator so need to call it in a for loop. (see main section)
	"""
	f=open(datfile, 'r')
	print('File opened...')
	flag = True
	while flag:
		try:
			print('Unpickling data...')
			data_chunk = cpk.load(f)
			yield(data_chunk)
		except EOFError:
			print('Reached end of file, no more data...')
			flag=False
	f.close()
	print('File closed...')

if __name__=='__main__':
	import sys
	pickled_ssfiles = sys.argv[1]
	
	print('Using "unpickle_chunk" generator...')
	#This is how to call 'unpickle_chunk' as it is a generator
	for chunk in unpickle_chunk(pickled_ssfiles):
		print(len(chunk), chunk[1])
		
	print('Using "unpickle_file" function...')
	#this is how to call 'unpickle_file'
	alldata = unpickle_file(pickled_ssfiles)
	for data_chunk in alldata:
		print(len(data_chunk), data_chunk[1])