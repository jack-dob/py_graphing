#!/Library/Frameworks/Python.framework/Versions/Current/bin//python

def read_dust_files(dust_files):
	block = []
	for file in dust_files:
		square = []
		#print(file)
		f = open(file, 'r')
		for aline in f:
			bline = aline.split()
			#print(bline)
			row = []
			if(bline[0]=='Trash'):
				row.append(-1)
			else:
				row.append(int(bline[0]))
			row += map(float, bline[1:])
			square.append(row)
		block.append(square)
	#block = [file_1_square, file_2_square, ... file_n_square]
	#file_m_square = [row_1, row_2, ... row_n]
	#row_m = [bin_num, dust_mass, %from_1, %from_2, ... %from_n]
	return(block)

if __name__=="__main__":
	import sys, os, math
	import numpy as np
	
	#sort arguments
	dust_files = []
	output_file = []
	for arg in sys.argv[1:]:
		if '.dust' in arg:
			dust_files.append(arg)
		else:
			output_file.append(arg)
	
	if len(output_file) > 1:
		sys.exit("Error: Can only output to one file")
	
	print("dust files:", dust_files)
	
	print("output:", output_file)
	block = read_dust_files(dust_files)
	
	i=0
	for file in block:
		print("filename:", dust_files[i])
		#for row in file:
			#print(row[0], row[1], np.sum(row[2:]))
		total_mass = np.sum([row[1] for row in file])
		print("total dust mass:",  total_mass)
		i+=1
	