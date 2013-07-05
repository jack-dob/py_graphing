#!/Library/Frameworks/Python.framework/Versions/Current/bin//python

def sort_args(arg_list):
	for arg in arg_list:
		if "alb" in arg:
			alb_file=arg
		elif "ext" in arg:
			ext_file=arg
		else:
			tag = arg
			
	return(alb_file, ext_file, tag)

def read_format(a_file):
	try:
		f = open(a_file, 'r')
	except IOError:
		print("Error: could not read file %s", afile)
		sys.exit(1)
	
	f.readline() #ignore first line
	sizes = f.readline().split()[1:] #read in this stuff, ignore the first column
	f.readline() #ignore the third line
	
	wavlns = []
	props = []
	for aline in f:
		bline = aline.split()
		wavlns.append(bline[1])#ignore 1st column, 2nd column is wavelengths
		props.append(bline[2:])#3rd column onwards is the data we want
	#print(wavlns)
	#print(props[0])
	
	half_way = []
	for i in xrange(len(props)):
		temp = []
		for item in props[i]:
			temp.append([wavlns[i], item])
		half_way.append(temp)
	
	#print(half_way[0])
	
	data = []
	for i in xrange(len(sizes)):
		temp=[part[i] for part in half_way]
		data.append([sizes[i], temp])
	
	#now is in format data=[ [size1, [[wav1_1, opac1_1], [wav1_2, opac1_2]...]],
	#						 [size2, [[wav2_1. opac2_1], [wav2_2, opac2_2]...]], ...]
	
	return(data)
	
def unpack_opac(alb_file, ext_file):
	
	alb_dat = read_format(alb_file)
	ext_dat = read_format(ext_file)
	
	#want format data=[ [size, [wav, alb, ext]], [size, [wav, alb ext]], ... ]
	if len(alb_dat) != len(ext_dat):
		print('Error: lenghts of data do not match! Exiting...')
		sys.exit()
	#print(alb_dat[0])
	data = []
	for i in xrange(len(alb_dat)):
		temp1 = [[wav1, alb, ext] for wav1, alb, wav2, ext in [thing+item for thing, item in zip(alb_dat[i][1], ext_dat[i][1])]]
		#print(temp1)
		#return
		data.append([alb_dat[i][0], temp1])
	#print(data[0])
		
	return(data)
		
		
def output_radmc(data, tag):
	#stuff goes here, read radmc3d manual for proper format
	#is in format data=[ [size, [wav, alb, ext]], [size, [wav, alb ext]], ... ]
	
	shortname = 'dustkappa_'+tag
	
	for datum in data:
		longname = shortname+datum[0]+'.inp'
		f=open(longname, 'w')
		f.write('2\n')
		f.write('{}\n'.format(str(len(datum[1]))))
		#scattering albedo = scattering/extinction
		#scattering = scattering albedo*extinction
		#absorption = extinction - scattering
		for wav, alb, ext in datum[1]:
			sca = float(alb)*float(ext)
			abs = str(float(ext) - float(sca))
			f.write("{}\t{}\t{}\n".format(wav, abs, sca))
		f.close()
	return
		
		
if __name__=="__main__":
	import sys, os
	
	#alb = albedo, ext = extinction
	alb_file, ext_file, tag = sort_args(sys.argv[1:])
	
	opac_info = unpack_opac(alb_file, ext_file)
	
	output_radmc(opac_info, tag)
	
	
		
		
		
		
		
		
		
		