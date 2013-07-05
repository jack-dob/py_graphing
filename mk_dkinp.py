#!/Library/Frameworks/Python.framework/Versions/Current/bin//python


def create_dustopac(dk_files):
	f = open('dustopac.inp', 'w')
	f.write('2\n') #format of this file, is always 2
	n_files = len(dk_files)
	f.write('%d\n'%(n_files)) #the number of different dust species
	dust_dat=[]
	for afile in dk_files:
		f.write('------------------------------\n') #line break
		ident = afile[10:-4] # the <name> part of 'dustkappa_<name>.inp
		f.write('1\n') #input style of dust file, is always 1 for 'dustkappa' type files
		f.write('0\n') #use quantum heating? always zero -> not implemented
		f.write('%s\n'%(ident)) # identifier of dust species
		dust_dat.append(ident.split('_'))
	f.write('------------------------------\n') #line break, you seem to need one at the end
	f.close() #close the file
	print('written dustopac.inp file.')
	return(dust_dat) #kicks out data about dust files in [type, size] style in order

def read_dustopac(dopac_file):
	f = open(dopac_file, 'r')
	dust_dat = []
	f.readline()
	n_dust = int(f.readline())
	for i in range(0, n_dust):
		f.readline()
		f.readline()
		f.readline()
		ident = f.readline()
		tag, size = ident.split('_')
		if tag=="AC1":
			factor = 0.8
		elif tag=="sil":
			factor = 0.2
		else:
			factor = 1.0
		dust_dat.append([factor, tag, float(size)])
	f.close()
	return(dust_dat)
	
	
	
	
if __name__=='__main__':
	import sys, os
	'''
	mk_dkinp.py [dustkappa files]
	
	dustkappa files: files that have the signature dustkappa_<name>.inp
	
	will use these files to create dustopac.inp file
	'''
	dk_files = sys.argv[1:]
	create_dustopac(dk_files)
	