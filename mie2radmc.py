#!/Library/Frameworks/Python.framework/Versions/Current/bin//python

def output_radmc(data, tag):
	#stuff goes here, read radmc3d manual for proper format
	#is in format data=[ [size, [wav, abs, sca]], [size, [wav, abs, sca]], ... ]
	
	shortname = 'dustkappa_'+tag
	
	for datum in data:
		longname = shortname+datum[0]+'.inp'#adds size information
		f=open(longname, 'w')
		f.write('2\n')
		f.write('{}\n'.format(str(len(datum[1]))))
		for wav, abs, sca in datum[1]:
			f.write("{}\t{}\t{}\n".format(wav, abs, sca))
		f.close()
		print("written to file {}".format(longname))
	return

def get_lambdas(size, x_list, abs_list, sca_list):
	import math
	
	#print(len(x_list), len(abs_list), len(sca_list))
	#print(x_list)
	#assuming lambdas are in micrometers
	#x=2*pi*a/lambda
	lam_list = ["%.6e"%(2.0*math.pi*float(size)/float(x)) for x in x_list]
	las_list=[]
	#for i in xrange(len(lam_list)):
	#	las_list.append([lam_list[i], abs_list[i], sca_list[i]])
	las_list = [[l, a, s] for l, a, s in zip(lam_list, abs_list, sca_list)]
	#print('HERE',las_list)
	return(las_list)

def mie2radmc(mie_file, sizes, tag):
	try:
		f = open(mie_file, 'r')
	except IOError:
		print("Error: Could not open file %s", mie_file)

	#print(sizes)
	x_list=[]
	ext_list=[] #extinction = scattering + absorbtion(1 - angle)
	sca_list=[] #scattering
	ang_list=[] #scattering angle
	f.readline() #ignore 1st line
	for aline in f:
		bline = aline.split()
		x_list.append(bline[0])
		ext_list.append(bline[1])
		sca_list.append(bline[2])
		ang_list.append(bline[3])
	#print(x_list)
	#print(ext_list)
	#print(sca_list)
	data=[]
	#x = 2*pi*a/lambda
	#extinction = absorbtion + scattering(1-angle)
	#absorption = extinction - scattering(1-angle)
	abs_list = [str(float(ext) - float(sca)*(1.0 - float(ang))) for ext, sca, ang in zip(ext_list, sca_list, ang_list)]
	
	for each_size in sizes:
		datum = get_lambdas(each_size, x_list, abs_list, sca_list)
		data.append([each_size, datum])
	#print(data[0])
	output_radmc(data, tag)
	return

if __name__=="__main__":
	import os, sys
	
	"""
	mie2radmc.py [mie_file] [tag] [sizes] 
	[mie_file]	file with mie-scattering data
	[tag]		tag to identify dust species by
	[sizes]		a list of sizes to create files for
	
	"""
	print("Note: Make sure your sizes are in MICROMETERS")
	mie_file = sys.argv[1]
	tag = sys.argv[2]
	sizes = sys.argv[3:]
	
	mie2radmc(mie_file, sizes, tag)
	
	