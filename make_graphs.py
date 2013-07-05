#!/Library/Frameworks/Python.framework/Versions/Current/bin//python


def FUNCTION_NAME(data_chunk):
	"""
	This function should create a data point for each time step
	"""
	return(0)

if __name__=='__main__':
	import sys, os, math
	import matplotlib as mpl
	import matplotlib.pyplot as plt
	import sys_to_si as s2s
	from readss import unpackxdr
	from unpickle_chunk import unpickle_chunk
	from eVa_graph import plot_eVa
	from mVa_graph import mVa_graph
	from surf_density import surf_density
	from RV_graph import plot_RV
	from energyVtime_graph import store_energy, plot_energy
	from count_ejected import store_ejected, plot_ejected
	
	"""
	This should let you create multiple plots of data whilst only having
	to unpickle the '.dat' file once.
	Will create numbered figures and close them after use for more info see:
	http://matplotlib.sourceforge.net/api/pyplot_api.html#matplotlib.pyplot.figure
	
	"""
		
	#This list holds the label of a graph and the name of the function to
	#call it's creation.
	graphlist = [	('ejected',store_ejected),
					('eVa',plot_eVa),
					('mVa', mVa_graph),
					('surfD',surf_density),
					('energy',store_energy),
					('RV', plot_RV)
				]
	#for the graphs that need data accross the whole time series, store the
	#name of the function that plots end graph.
	alltimedict = 	{	store_energy:plot_energy,
						store_ejected:plot_ejected
					}
	#assume data file is in first argument, output folder is in last arg
	if len(sys.argv)>2:
		#this is the top level folder for the directory tree
		outfolder = os.path.normpath(sys.argv[-1])
		print(outfolder)
		print(sys.argv[1:-1])
	else:
		print('ERROR: Need an output folder to store all this data')
		sys.exit(1)

	if 'y'!=raw_input("Have you modified the source code so you don't overwrite stuff? <y/n> ")[0]:
		print("Then do that now.\n")
		sys.exit(0)
	print('Good.\n')
	
	if not os.path.exists(outfolder):
		if 'y'==raw_input("Destination folder does not exist, create it? <y/n> "):
			print('Creating top level destination folder...')
			os.makedirs(outfolder)
		else:
			print("Please choose an exsisting destination folder.")
			sys.exit(0)
	for label, function in graphlist:
		if function in alltimedict and os.path.exists(os.path.join(outfolder,label,'temp')):
			#delete old temporary storage space
			os.system('rm '+os.path.join(outfolder,label,'temp'))
	
	if '.dat' in sys.argv[1]:
		for data_chunk in unpickle_chunk(sys.argv[1]):
			#create identity string for each graph (timestamp)
			#time from these files is in "system time" in units of years*2*pi
			#therefore need to divide by 2*pi to make numbers correct
			ident_string = 'ss.{0:08.3f}'.format(s2s.year(data_chunk[1]))
			for label, function in graphlist:
				#each set of graphs draws to different figures
				plt.figure(graphlist.index((label,function)))
				if not os.path.exists(os.path.join(outfolder,label)):
					#make the second level folders if they don't exist
					os.mkdir(os.path.join(outfolder,label))
				if function in alltimedict:
					#if graph is using data from entire time series, 
					#create a temporary storage file
					outname=os.path.join(outfolder,label,'temp')
				else:
					#if graph is made new each time, stamp graph name with
					#timestamp
					outname = os.path.join(outfolder,label,ident_string+'.png')
				#execute the function that creates the graph/datapoint
				function(data_chunk, outfname=outname)
	else:
		for arg in sys.argv[1:-1]:
			for data_chunk in [unpackxdr(arg)]:
				#create identity string for each graph (timestamp)
				#time from these files is in "system time" in units of years*2*pi
				#therefore need to divide by 2*pi to make numbers correct
				ident_string = 'ss.{0:08.3f}'.format(s2s.year(data_chunk[1]))
				for label, function in graphlist:
					#each set of graphs draws to different figures
					plt.figure(graphlist.index((label,function)))
					if not os.path.exists(os.path.join(outfolder,label)):
						#make the second level folders if they don't exist
						os.mkdir(os.path.join(outfolder,label))
					if function in alltimedict:
						#if graph is using data from entire time series,
						#create a temporary storage file
						outname=os.path.join(outfolder,label,'temp')
					else:
						#if graph is made new each time, stamp graph name with
						#timestamp
						outname = os.path.join(outfolder,label,ident_string+'.png')
					#execute the function that creates the graph/datapoint
					function(data_chunk, outfname=outname)
				
	for label, function in graphlist:
		if function in alltimedict:
			#move to the correct figure
			plt.figure(graphlist.index((label,function)))
			#now draw the graph from the stored data
			alltimedict[function](os.path.join(outfolder,label,'temp'),outfname=os.path.join(outfolder,label,label+'.png'))
			#move the temporary storage space to 'raw.dat'
			os.system('mv '+os.path.join(outfolder,label,'temp')+' '+os.path.join(outfolder,label,'raw.dat'))
			
	plt.close('all')#close all active figures
