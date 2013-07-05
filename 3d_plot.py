#!/Library/Frameworks/Python.framework/Versions/Current/bin//python

import matplotlib.pyplot as plt
import matplotlib.figure as fig
from readss import unpackxdr
from unpickle_chunk import unpickle_chunk
import sys, os, math
import sys_to_si as s2s

def grab_data(pdata):
	xs=[]
	ys=[]
	zs=[]
	sizes=[]
	colours=[]
	colour_list = ['k','w','r','g','b','y','m','c','g','p','o','br']
	mass_min = min([m[0] for m in pdata])
	mass_max = max([m[0] for m in pdata[1:]]) #ignore planet
	#mass_max = 1
	rad_min = min([r[1] for r in pdata])
#	0=BLACK,1=WHITE,2=RED,3=GREEN,4=BLUE,5=YELLOW,6=MAGENTA,7=CYAN,
#         8=GOLD,9=PINK,10=ORANGE,11=KHAKI,12=VIOLET,13=MAROON,14=AQUA,
#         15=NAVY,16=BLACK,17-254=INCREASING GRAY,255=WHITE
	i=0
	for particle in pdata:
		#use this if jupiter is taking over the whole screen
		'''
		if i==0:
			i+=1
			continue
		'''
		#use this if everything is taking a long time to display
		'''
		if (i/10.0)!=round((i/10.0)):
			i+=1
			continue
		'''
		
		#Do this if using a solar system file, this will stop loads of ejected stuff being displayed
		
		if sum([x*x for x in particle[2]])>40:
			i+=1
			continue
		
		#sizes.append(0.1*particle[0]/(mass_min)) 	# size of point proportional to mass
		#sizes.append(0.1*particle[1]/rad_min)		# may need to use a sqrt or cbrt scale due to area/volume viewin, perhaps log? 
		'''
		xs.append(s2s.dist(particle[2][0]))
		ys.append(s2s.dist(particle[2][1]))
		zs.append(s2s.dist(particle[2][2]))
		'''
		xs.append(particle[2][0])
		ys.append(particle[2][1])
		zs.append(particle[2][2])
		#print("position of particle ",i," is ", map(s2s.dist,particle[2]), particle[2])
		if particle[0] > mass_max:
			sizes.append(0.1*particle[1]/rad_min)
		elif particle[0] > mass_min:
			sizes.append(5*particle[1]/rad_min)
		else:
			sizes.append(0.1*particle[1]/rad_min)
		colours.append(round(5.0*(particle[0]-mass_min)/mass_max)) #100 steps
		i+=1
		
	print("Minimum radius is", rad_min, " in si ", s2s.dist(rad_min) )
	print("Minimum mass is", mass_min, " in si ", s2s.mass(mass_min) )
	print("Maximum mass is", mass_max, " in si ", s2s.mass(mass_max))
	print("Lenght of arrays:", len(zs))
	return(xs, ys, zs, sizes, colours)
		
		
def plot_3d(data_chunk, outfname):
	from mpl_toolkits.mplot3d import Axes3D
	cm = plt.get_cmap("jet")
	(pdata, systime, particle_num) = data_chunk
	#this_fig = plt.Figure()
	fig.Figure.delaxes(plt.gcf(), plt.gca())
	#fig.Figure.clear(plt.gcf()) #clear the current figure
	print("Making 3D plot...")
	
	ax = plt.gcf().add_subplot(111, projection='3d')

	(xs, ys, zs, sizes, colours) = grab_data(pdata)
	
	#for debugging
	'''
	xs = [0, 1]
	ys = [0, 0]
	zs = [2, 4]
	sizes = [1, 4]
	colours = ['g', 'g']
	'''
	three_d = ax.scatter(xs, ys, zs, s = sizes, c = colours, cmap = cm, marker='o', edgecolors='none')
	
	ax.set_xlabel('Displacement (m)')
	ax.set_ylabel('Displacement (m)')
	ax.set_zlabel('Displacement (m)')
	three_d.set_clim(0, 5)
	#plt.colorbar()
	#plt.axis([0,5,-0.05,1])
	
	if outfname==None:
		plt.show()
	else:
		plt.savefig(outfname)
		
	return(0)

if __name__=="__main__":

	print("Starting 3d plotting, patience is a virtue...")
	
	if len(sys.argv)>2:
		outpath = sys.argv[-1]
		amax = -1
	else: 
		outpath = None
		amax = 2
	
	if outpath=='None' or outpath=='none' or outpath=='NONE':
		outpath = None
	
	if '.dat' in sys.argv[1]:
		for data_chunk in unpickle_chunk(sys.argv[1]):
			ident_string = 'ss.{0:06.5f}'.format(data_chunk[1])
			outname = os.path.join(outpath,ident_string+'.png')
			plot_3d(data_chunk, outfname=outname)
	else:
		for arg in sys.argv[1:amax]:
			data_chunk = unpackxdr(arg)
			ident_string = 'ss.{0:06.5f}'.format(data_chunk[1])
			if outpath != None:
				outname = os.path.join(outpath,ident_string+'.png')
			else: outname = None
			plot_3d(data_chunk, outfname=outname)
