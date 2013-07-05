#!/usr/bin/python
def unpackxdr_head(ssfile):
	import sys
	import xdrlib as xdr
	print('In unpackxdr...')
	f =  open(ssfile, 'rb')
	data = f.read(16)
	xfile = xdr.Unpacker(data)
	f.close()

	#this stuff is the header data
	time = xfile.unpack_double() #8 bytes
	particle_num = xfile.unpack_int() #4bytes
	xfile.unpack_int()#unused padding number, 4butes, keeps everything in 8byte blocks
	print('Time index is %lf, total number of particles is %i' %(time, particle_num))
	try:
		xfile.done()
		print("\nFinished Unpacking Header")
	except xdr.Error:
		print("\nError: Something wierd happened")
	
	return(None, time, particle_num) # 3 return parameters, same as unpackxdr()
	
def unpackxdr(ssfile):
	import sys
	import xdrlib as xdr
	print('In unpackxdr...')
	f =  open(ssfile, 'rb')
	data = f.read()
	xfile = xdr.Unpacker(data)
	f.close()

	#this stuff is the header data
	time = xfile.unpack_double()
	particle_num = xfile.unpack_int()
	xfile.unpack_int()#unused padding number, keeps everything in 8byte blocks
	print('Time index is %lf, total number of particles is %i' %(time, particle_num))
	plist = []

	for i in xrange(0,particle_num):
		plist.append([	
		xfile.unpack_double(),#mass
		xfile.unpack_double(),#radius
		[xfile.unpack_double(),xfile.unpack_double(),xfile.unpack_double()],#positon [x,y,z]
		[xfile.unpack_double(),xfile.unpack_double(),xfile.unpack_double()],#velocity [x,y,z]
		[xfile.unpack_double(),xfile.unpack_double(),xfile.unpack_double()],#spin [x,y,z]
		xfile.unpack_int(),#colour
		xfile.unpack_int()]#orignal_index, position is current index
		)
		sys.stdout.write('\r%i particles unpacked...' %i)

	try: 
		xfile.done()
		print('\nFinished Unpacking')
	except xdr.Error:
		print('\nError: "particle_num" != length of file...')

	#plist = list of particles with their properties etc (see SSDATA in c files)
	return(plist, time, particle_num)

def packxdr(ssfile, data, del_list=[]):
	import sys, os
	import xdrlib as xdr
	from types import *
	
	if os.path.exists(ssfile):
		response=[None]
		while response[0]!='y' and response[0]!='n':
			response = raw_input('This file exsists, are you sure you want to overwrite it? <y/n>')
			print(response)
		if response == 'n': sys.exit(1)

	
	xpac = xdr.Packer()

	xpac.pack_double(data[1])
	xpac.pack_int((data[2]-len(del_list)))
	xpac.pack_int(-1)
	print('Writing particles...')
	i=1
	for particle in data[0]:
		if particle[6] in del_list: continue
		for lump in particle:
			if type(lump)==FloatType:
				xpac.pack_double(lump)
			if type(lump)==ListType:
				for thing in lump:
					xpac.pack_double(thing)
			if type(lump)==IntType:
				xpac.pack_int(lump)
		sys.stdout.write('\r%i particles packed...' %i)
		i+=1
	sys.stdout.write('\n')
	f =  open(ssfile, 'wb')
	f.write(xpac.get_buffer())
	f.close()
	return(True)
	
if __name__=='__main__':
	import os, sys

	for arg in sys.argv[1:]:
		do_something = unpackxdr(arg)
						
