#!/Library/Frameworks/Python.framework/Versions/Current/bin//python
VERBOSE=True

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
	
def this(num):
	if(VERBOSE): print(num)
	return(float(num))
	
	
if __name__=='__main__':
	import sys, os
	'''
	renames files via numerical sequence.
	enter suffixes and prefixes as strings e.g. 'asuffix'
	this way can have no suffix by passing empty string e.g. ''
	
	rename.py [folder] [prefix] [suffix]
	'''
	filelist = os.listdir(sys.argv[1]) #list files in directory given
	pf_len = len(sys.argv[2]) #2nd arg is prefix to file pattern
	sf_len = len(sys.argv[3]) #3rd arg is suffix to file pattern
	#get a sorted list of the numbers so can iterate through
	filelist = [name for name in filelist if ((name[:pf_len]==sys.argv[2]) and 
												(name[-sf_len:]==sys.argv[3]))]
	numlist = [name[pf_len:-(sf_len)] for name in filelist]
	#print(numlist[0], filelist[:5])
	numlist = [this(num) for num in numlist]
	file_dict = dict(zip(numlist, filelist)) # match up the numbers to the files
	numlist.sort() #as usually the file names are time-stamped so this will sort in time order
	# can then use numlist to sort dictionary
	
	if(VERBOSE): print(numlist)
	if(VERBOSE): print(file_dict)
	#sys.exit(0)
	#i=0	
	for num, file in file_dict.items():
		#fname = sys.argv[2]+str(num)+sys.argv[3]
		newfname = sys.argv[2]+eval("'{0:0'+str(len(str(len(numlist))))+'d}'")+sys.argv[3]
		newfname = newfname.format(numlist.index(num))
		os.system('mv -f '+sys.argv[1]+file+' '+sys.argv[1]+newfname)
		#print('mv -f '+sys.argv[1]+file+' '+sys.argv[1]+newfname)
		#i+=1
	