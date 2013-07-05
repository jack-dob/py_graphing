#!/Library/Frameworks/Python.framework/Versions/Current/bin//python

def plot_stuff(data, outfname=None):
	import sys_to_si as s2s
	import matplotlib.pyplot as plt
	import matplotlib.figure as fig
	
	fig.Figure.clear(plt.gcf())
	F=plt.gcf()
	print('Plotting data...')
	data = zip(*datas)
	data2 = []
	for chunk in data:
		#print(chunk)
		#print(chunk[0])
		data1 = []
		for lump in chunk:
			#print(lump)
			data1.extend(lump)
		#print(data1)
		data2.append(data1)
		#sys.exit()
	data = data2
	#print(data)
	x = 0
	y = 1
	
	print(data[0])
	plt.loglog([datum[x] for datum in data],[datum[y] for datum in data], label= 'Flux', linewidth=2.0) 
	#plt.loglog([datum[x] for datum in data],[datum[y+1] for datum in data], label = 'Density') 
	#plt.plot([datum[x] for datum in data],[datum[y+2] for datum in data], label = 'pressure') 
	#plt.plot([datum[2] for datum in data],[datum[4] for datum in data]) 
	#plot the data, 'zorder=0' makes sure that it is drawn first and everything else is on top of it

	#plt.legend()
	plt.xlabel('Wavelength (micrometers)', fontsize=24)
	plt.ylabel('erg cm$^{-2}$ s$^{-1}$ Hz$^{-1}$', fontsize=24)
	plt.tick_params(axis='both', which='major', labelsize=18)
	dpi = F.get_dpi()
	F.set_size_inches(800/dpi, 800/dpi)
	if outfname==None:
		plt.show()
		return(0)
	else:
		plt.savefig(outfname, bbox_inches='tight')
		return(0)

if __name__=='__main__':
	import matplotlib.pyplot as plt
	from readss import unpackxdr
	from unpickle_chunk import unpickle_chunk
	import sys, os, math
	
	if(len(sys.argv) > 2):
		outfname = sys.argv[-1]
		args = sys.argv[1:-1]
	else:
		outfname=None
		args=sys.argv[1:]
	
	lims = [(3, 1000), (3,10000), (3, 10000)]
	datas= []
	j=0
	for arg in args:
		f = open(arg)
		data = []
		i=0
		for aline in f:
			if (i>=lims[j][0]) and (i<=lims[j][1]):
				data.append(aline.split())
			i+=1
		i+=1
		datas.append(data)
	#datas = zip(*datas)
	plot_stuff(datas, outfname=outfname)
