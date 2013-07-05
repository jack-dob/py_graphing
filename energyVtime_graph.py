#!/Library/Frameworks/Python.framework/Versions/Current/bin//python

def inst_energy(mass, pos, vel):   
    from math import sqrt
    from eVa_graph import inst_e
    #remember m is in solar masses, pos in AU, speed in AU/(2PI*yr)
    #-2Gm1m2/r+1/2(m1V1*V1+m2*V2*V2) = total energy
    spd2 = sum([veli*veli for veli in vel])
    r2=sum([posi*posi for posi in pos])
    G = 1.0 #grav const =1 in the sim for less operations, M is in solar masses, so M=1
    T = 0.5*mass*spd2 #solar contribution is negligible
    V = -G*mass/sqrt(r2)
    E = T+V
    return(E)
    

def get_energy(data_chunk):
	import sys
	import sys_to_si as s2s
	print("Finding energy of system...")
	(pdata, time, N_p) = (data_chunk[0], data_chunk[1], data_chunk[2])
	rockE = []
	planetE=[]
	for m, r, pos, vel, spn, col, idx in pdata:
		if col!=3: 
			planetE.append(inst_energy(m, pos, vel))
			#print(sum([posi*posi for posi in pos]))
		else: rockE.append(inst_energy(m,pos,vel))
		
	#print(time, sum(rockE), planetE[0])
	return(s2s.year(time) ,sum(rockE)+sum(planetE), sum(rockE), sum(planetE))
	
def store_energy(data_chunk, outfname=None):
	import cPickle as cpk #use this as can store complete precision
	print("Storing energy point...")
	f=open(outfname,'a')
	cpk.dump(map(float,get_energy(data_chunk)),f, cpk.HIGHEST_PROTOCOL)
	f.close()
	
def plot_energy(infname, outfname=None):
	import cPickle as cpk #use this as can store complete precision
	import matplotlib.pyplot as plt
	
	if outfname==None:
		f = open(infname, 'r')
		outfname = infname
		
	f = open(infname, 'r')
	data = []
	
	while True:
		try: apoint = cpk.load(f)
		except EOFError: break
		data.append(apoint)
	data.sort()
	#print(data)
	f.close()
	plt.plot([x[0] for x in data],[y[2] for y in data], 'r-.', label="Planetesimal Energy")
	plt.plot([x[0] for x in data],[y[3] for y in data], 'b-.', label="Planet Energy")
	plt.plot([x[0] for x in data],[y[1] for y in data], 'g-', label="Total Energy")

	'''
	plt.plot(data[0], data[1], 'g-', label="Total Energy")
	plt.plot(data[0], data[2], 'r-.', label="Planetesimal Energy")
	plt.plot(data[0], data[3], 'b-.', label="Planet Energy")
	'''
	plt.legend(loc=4)
	plt.title('Total energy of system')
	plt.xlabel('Time (Years)')
	plt.ylabel('Energy (arb. units)')
	if outfname==None:
		plt.savefig(infname)
	else:
		plt.savefig(outfname)
			 
		
		

if __name__=='__main__':
	import matplotlib.pyplot as plt
	from readss import unpackxdr
	from unpickle_chunk import unpickle_chunk
	import sys, os, math
	
	if len(sys.argv)>2:
		outpath = sys.argv[-1]
	else: outpath = None
	
	
	E_list = []
		
	if '.dat' in sys.argv[1]:
		for data_chunk in unpickle_chunk(sys.argv[1]):
			E_list.append(plot_energy(data_chunk)) #get data for plot
			#print('Energy of system is {0}'.format(E_list))
	else:
		for data_chunk in [unpackxdr(sys.argv[1:-1])]:
			E_list.append(plot_energy(data_chunk)) #get data for plot
			#print('Energy of system is {0}'.format(E_list))
	
	E_list.sort() #sorts by first number in tuple (time)
	plt.plot([x[0] for x in E_list], [y[1] for y in E_list], 'g-', label='Total Energy')#total energy
	plt.plot([x[0] for x in E_list], [y[2] for y in E_list], 'r--', label='Planetesimal Energy') #planetesimal energy
	plt.plot([x[0] for x in E_list], [y[3] for y in E_list], 'b--', label='Jupiter Energy') #jupiter energy
	#plot the data, 'zorder=0' makes sure that it is drawn first and everything else is on top of it
	#plt.axis([0,5,0,1])
	
	plt.legend()
	plt.ticklabel_format(axis='y', scilimits=(-3,3))
	#put in lables and titles etc
	plt.title('Total energy of system')
	plt.xlabel('Time (Years)')
	plt.ylabel('Energy (arb. units)')
	
	
	if outpath==None: outname=None
	else: 
		ident_string = 'total_energy'
		outname = os.path.join(sys.argv[-1],ident_string+'.png')
	
	if outname==None:
		plt.show()
	else:
		plt.savefig(outname)


