#!/Library/Frameworks/Python.framework/Versions/Current/bin//python


def read_dust_density(fname):
	try:
		f = open(fname, "r")
	except IOError:
		print("Error: Could not open file");
		sys.exit()
	
	iformat = f.readline()
	nrcells = f.readline()
	nrspec = f.readline()
	data = []
	for aline in f:
		data.append(float(aline))
	return(iformat, nrcells, nrspec, data)


def write_dust_density(iformat, nrcells, nrspec, data, filename):
	try:
		f = open(fname, 'w')
	except IOError:
		print("Error: Could not open file for writing")
		sys.exit()
	
	f.write("{}\n".format(iformat))
	f.write("{}\n".format(nrcells))
	f.write("{}\n".format(nrspec))
	for dat in data:
		f.write("{}\n".format(dat))
	return()
		

def dd_factor(fname, factor):
	master = open(fname, 'r')
	slave = open(fname+'~', 'w')
	
	blob = master.readline() #iformat
	slave.write(blob)
	blob = master.readline() #nrcells
	slave.write(blob)
	blob = master.readline() #nrspec
	slave.write(blob)
	
	for aline in master: #density
		blob = float(aline)
		blob = blob*factor
		slave.write("{}\n".format(blob))
	
	master.close()
	slave.close()
	return()

if __name__=="__main__":
	import sys, os
	
	
	if(len(sys.argv)!=3):
		print("ERROR: Too few arguments, give path to dust_density.inp and muliplication factor")
	dd_file = sys.argv[1] #filename of dust_density.inp
	factor = float(sys.argv[2]) #the factor to multiply everything by
	print("Muliplying {} by {}".format(dd_file, factor))
	dd_factor(dd_file, factor)
	print("Finished.\a\a\a\a\a\a\a\a\a\a\a\a\a") #I like the bell sounds...
	#iformat, nrcells, nrspec, data = read_dust_density(dd_file)
	#data = [dat*factor for dat in data] #multiply by the factor
	#filename = dd_file+"~"
	#write_dust_density(iformat, nrcells, nrspec, data, filename)
	
	