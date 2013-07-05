#!/Library/Frameworks/Python.framework/Versions/Current/bin//python
##########################Start Star Class##########################
class Star:
	def __init__(self, temp=6000, type='G', spect_type=5, rad=7E8, metal=0.018):
		'''
		Create all obvious attributes
		'''
		import math
		self.temp = temp
		self.type = type
		self.spect_type = spect_type
		self.rad = rad
		self.metal = metal
		self.surf_area = 4/3*math.pi*rad*rad
		self.vol = 4*math.pi*rad*rad*rad
		self.wstart = 1E-10
		self.wstop = 1E-5
		self.wstep = 1E-10
		self.wFACTOR = 1.01
	
	def spect_flux(self, wavelth, modfunc=None):
		'''
		use planck law multiplied by surface area of particles, if the
		surface area of particles is larger than the geometrical area of 
		the annulus we're in, use geometry instead (particles occlude eachother)
		'''
		if modfunc==None:
			return(wavelth*1E9, self.surf_area*planck(wavelth, self.temp))
		else:
			return(wavelth*1E9, modfunc(wavelth)*self.surf_area*planck(wavelth, self.temp))
	
	def spect_dist(	self, modfunc=None):
		'''
		loops over wavelength range (in meters) to give a
		wavelength, flux pair. Takes a modifier function to be
		adjust output for albedo, adsorpivity, emissivity etc.
		'''
		#print('HERE',modfunc)
		if modfunc==None:
			for wavelth in frange(	self.wstart, self.wstop, self.wstep,
									Factor=self.wFACTOR):
				a = self.spect_flux(wavelth)
				yield(a[0], a[1])
				
		else:
			for wavelth in frange(	self.wstart, self.wstop, self.wstep,
									Factor=self.wFACTOR):
				a = self.spect_flux(wavelth)
				yield(a[0], modfunc(wavelth)*a[1])
	
	def my_sb(self, modfunc=None):
		if modfunc==None: return(5.67E-8)
		else:
			p=self.power(modfunc)
			
			
	def plot_spect(self, *args, **kwargs):
		'''
		Plots spectra, sends any arguments (norm and keyword) to plt.plot()
		function.
		'''
		import matplotlib.pyplot as plt
		plt.plot(	[a[0] for a in self.spect_dist()],
					[a[1] for a in self.spect_dist()], *args, **kwargs)
	
	def power_sb(self):
		'''
		Uses Steffan-Boltzmann law to find the power output of
		planck law
		'''
		s_b_const = 5.67E-8
		return(s_b_const*self.temp*self.temp*self.temp*self.temp*self.surf_area)
	
	def weighting_ftn(self, wavelth):
		return(self.surf_area)
		
	def power(self, modfunc=None):
		'''
		Integrates spect_dist to get power, if modfuc==None, uses
		stefan-boltzmann law.
		Need 1/1E9 factor because of output from spect_flux is in nm
		'''
		import scipy.integrate as spi
		import numpy as np
		
		if modfunc==None: 
			print('pwr',self.power_sb())
			return self.power_sb()
		else:
			a = [b for b in self.spect_dist(modfunc)]
			print(a[1])
			#p_t= spi.simps([b[1] for b in a],[b[0] for b in a])
			p_t=spi.fixed_quad(planck_wrap, 0, 0.01, args=(self.temp,
							self.weighting_ftn, modfunc), n=1000)
			print('pwr:', p_t)
			return(p_t[0])
			
	def wavelth_max(self):
		'''
		Finds the wavelength of peak emission (Wien Displacement)
		'''
		b = 3E-3
		return(b/self.temp)
	
	def peak_flux(self):
		'''
		Wraps 'wavelth_max()' to get peak power output
		'''
		return(self.spect_flux(self.wavelth_max())[1])
##########################End Star Class##########################


##########################Start Reflector Class##########################
class Reflector:
	def __init__(self, dist=1.5E11, star=Star(), rad=1E-6):
		'''
		Create all obvious attributes
		'''
		import math
		self.star = star
		self.dist = dist
		self.rad = rad
		self.surf_area = 4/3*math.pi*rad*rad
		self.temp = self.equib_temp()
		self.dr = 1.5E9 #(1/100th of an AU)
		self.density=1000 #kg m^-3
		self.vol = 4*math.pi*rad*rad*rad
		self.mass = self.vol*self.density
		self.wstart = 1E-10
		self.wstop = 1E-5
		self.wstep = 1E-10
		self.wFACTOR = 1.01
		
	def albedo(self, wavelth):
		'''
		This defines the reflectiviy at a given wavelength, will need to
		model this accurately
		'''
		return(0.3) #kinda brown
	
	def absorpivity(self, wavelth):
		'''
		this defines how well an object absorbs at a given wavelength,
		usually assume absorbs everything it doesn't reflect
		'''
		return(1.0)#-self.albedo(wavelth))
		
	def emissivity(self, wavelth):
		'''
		This defnes how well an object emmits at a given wavelength, usually
		is defined as a constant (grey dust assumption)
		'''
		return(0.3) #1==black body
		
	def equib_temp(self):
		import math
		'''
		power in = power out
		'''
		modfunc1=None
		modfunc2=None
		
		p_in = self.star.power(modfunc=modfunc1)*self.rad*self.rad*(1/(self.dist*self.dist))
		print(p_in)
		#p_out = s_b_const*temp^4*area = p_in
		return(math.pow(p_in/(self.my_sb(modfunc=modfunc2)*self.surf_area),0.25))
	
	def spect_flux(self, wavelth, modfunc=None):
		'''
		use planck law multiplied by surface area of particles, if the
		surface area of particles is larger than the geometrical area of 
		the annulus we're in, use geometry instead (particles occlude eachother)
		'''
		import sys, math
		NA = self.surf_area*self.num_particles()
		GA = math.pi*(2*self.dist*self.dr+self.dr*self.dr)
		if NA > GA: 
			#sys.stdout.write('Particles are obscuring each other, adjusting...\r')
			NA = GA
		if modfunc==None:
			return(wavelth*1E9, NA*planck(wavelth, self.temp))
		else:
			return(wavelth*1E9, modfunc(wavelth)*NA*planck(wavelth, self.temp))
	
	def spect_dist(	self, modfunc=None):
		'''
		loops over wavelength range (in meters) to give a
		wavelength, flux pair. Takes a modifier function to be
		adjust output for albedo, adsorpivity, emissivity etc.
		'''
		#print('HERE',modfunc)
		if modfunc==None:
			for wavelth in frange(	self.wstart, self.wstop, self.wstep,
									Factor=self.wFACTOR):
				a = self.spect_flux(wavelth)
				yield(a[0], a[1])
				
		else:
			for wavelth in frange(	self.wstart, self.wstop, self.wstep,
									Factor=self.wFACTOR):
				a = self.spect_flux(wavelth)
				yield(a[0], modfunc(wavelth)*a[1])
	
	def my_sb(self, modfunc=None):
		if modfunc==None: return(5.67E-8)
		else:
			p=self.power(modfunc)
			
			
	def plot_spect(self, *args, **kwargs):
		'''
		Plots spectra, sends any arguments (norm and keyword) to plt.plot()
		function.
		'''
		import matplotlib.pyplot as plt
		plt.plot(	[a[0] for a in self.spect_dist()],
					[a[1] for a in self.spect_dist()], *args, **kwargs)
	
	def power_sb(self):
		'''
		Uses Steffan-Boltzmann law to find the power output of
		planck law
		'''
		s_b_const = 5.67E-8
		return(s_b_const*self.temp*self.temp*self.temp*self.temp*self.surf_area)
	
	def power(self, modfunc=None):
		'''
		Integrates spect_dist to get power, if modfuc==None, uses
		stefan-boltzmann law.
		Need 1/1E9 factor because of output from spect_flux is in nm
		'''
		import scipy as sp
		
		if modfunc==None: 
			#print(self.power_sb())
			return self.power_sb()
		else:
			self.spect_flux(modfunc=modfunc)
			#print(p_t)
			return(p_t)
	
	def num_particles(self, total_mass = 4.7*6E24, power=-1):
		'''
		Uses total mass and power law to find mass in each annulus,
		then divides that by mass of dust particle to get number of dust
		particles in that annulus
		'''
		import math
		if power!=-1:
			A = math.pow(self.dist+self.dr/2, power+1)
			B = math.pow(self.dist-self.dr/2, power+1)
			const = total_mass*(power+1)/A
			M_ring = (const/(power+1))*(A-B)
		else:
			A = math.log(self.dist+self.dr/2)
			B = math.log(self.dist-self.dr/2)
			const = total_mass/A
			M_ring = const*(A-B)
		
		return(M_ring/self.mass)
	
	def wavelth_max(self):
		'''
		Finds the wavelength of peak emission (Wien Displacement)
		'''
		b = 3E-3
		return(b/self.temp)
	
	def peak_flux(self):
		'''
		Wraps 'wavelth_max()' to get peak power output
		'''
		return(self.spect_flux(self.wavelth_max())[1])
##########################End Reflector Class##########################
		
		
def frange(start, stop, step, Factor=1):
	'''
	Alternative range fuction, operates with floats and 
	supports geometrical progression of step sizes
	'''
	import sys
	precisionlist = []
	for num in (float(start),float(stop),float(step)):
		i=0
		while not num.is_integer():
			num*=10
			i+=1
		precisionlist.append(i)
	precision = max(precisionlist)+1
	if Factor==1:
		while start<stop:
			#sys.stdout.write("{0}   \r".format(start))
			yield(start)
			start+=step
			start = round(start,precision)
	else:
		while start<stop:
			#sys.stdout.write("{0}   \r".format(start))
			yield(start)
			start+=step
			step*=Factor
			start = round(start, precision)
	#print(list,len(list)) 	
	
	
def planck(wavelth, temp):
	'''
	Gives spectral radiance:
	Power per unit projected area, per unit solid angle, at a given frequency
	Computes Plancks Law.
	'''
	import numpy as np
	h = 6.26E-34 #planck constant
	c = 3E8 #speed of light
	K = 1.38E-23 #boltzmann constant
	
	A = (2*h*c*c)/(wavelth*wavelth*wavelth*wavelth*wavelth)
	try: B = c*h/(wavelth*K*temp) #if this is really big, answer will be really small
	except ZeroDivisionError: return(0)
	try: C = np.exp(B)-1 #if this is really big, answer will be really small
	except OverflowError: return(0)
	return(A*(1/C))

def planck_wrap(wavelth, temp, *args):

	p = planck(wavelth, temp)
	for arg in args:
		if arg==None:continue
		p*=arg(wavelth)
	return(p)

def add_specs(speclist):
	'''
	Adds spectra together.
	At the moment they must have the same range and sample points,
	could possibly write a wrapper to get around this.
	'''
	sumlist = []
	wavlist = []
	for i in xrange(0, len(speclist[0])):
		sumlist.append(0)
		wavlist.append(speclist[0][i][0])
		for specval in [a[i][1] for a in speclist]:
			sumlist[i]+=specval
	return (wavlist, sumlist)


def disk_sed(	dr = 1.5E4, start = 0.015*1.5E11, 
				gap_start = 0.05*1.5E11, gap_end=0.05*1.5E11,
				end = 15*1.5E11, FACTOR=1.1):
	'''
	Creates the Spectral Energy Distributions for each annulus of a
	dust disk. step is variable by use of 'frange' function so bottlenecks
	can be avoided when using small 'dr' step for close in regions.
	Uses the 'Reflector' class, will have to change this if want the functions
	that find the spectra to work differently.
	'''
	spect_dist_list=[] #create a container
	x_0 = start-dr #rember this number
	for x in frange(start, gap_start, dr, Factor=FACTOR):
		dust = Reflector(star=star1, dist=x) #create our test dust particle
		dust.dr=(x - x_0) #set the variable 'dr' correctly
		x_0 = x #reset x_0 to new value
		sys.stdout.write("{0:E}, {1:E}\r".format(
						dust.dist, dust.temp)) #debugging
		#add dust spectra to container
		spect_dist_list.append([a for a in dust.spect_dist()])
		
	x_1 = gap_end-dr #remember this number
	for x in frange(gap_end, end, dr, Factor=FACTOR):
		dust = Reflector(star=star1, dist=x) #create our test particle
		dust.dr=(x - x_1) #set attribute 'dr' correctly (pesky variable radial step)
		x_1 = x #reset x_1 to new value
		sys.stdout.write("{0:E}, {1:E}\r".format(
						dust.dist, dust.temp)) #debugging
		#add dust spectra to container
		spect_dist_list.append([a for a in dust.spect_dist()])
	#add all the spectra from each annulus together and return the whole thing
	return(add_specs(spect_dist_list))
		
		
if __name__=='__main__':
	import sys, os
	import matplotlib.figure as fig
	import matplotlib.pyplot as plt
	
	#Initialise stuff so don't have to find it in code
	dr = 1.5E4
	start = 0.015*1.5E11
	gap_start = 0.016*1.5E11
	gap_end=0.2*1.5E11
	end = 15*1.5E11
	FACTOR=1.1
	
	#clear the figure (it might be dirty...)
	fig.Figure.clear(plt.gcf())
	
	#create a star for our dust to be around
	star1 = Star(temp=6000, rad=1*7E8)
	#plot it's spectra
	star1.plot_spect('b-',linewidth=5, label='Stellar Flux')
	print('DONE THAT')
	#plt.show()
	#sys.exit(0)
	#print(star1.power())
	
	#make a list of the spectra of all the components
	component_spectra = []
	#add the star to list of components
	component_spectra.append([a for a in star1.spect_dist()])
	
	#create the disk sed
	a, b = disk_sed(dr=dr,start=start,
					gap_start=gap_start, gap_end=gap_end,
					end=end, FACTOR=FACTOR)
	#plot it
	plt.plot(a,b, 'g-', linewidth=5, label='Dust Flux')
	
	#add the disk to list of system components
	component_spectra.append([(i,j) for i,j in zip(a,b)])
	#print(component_spectra)
	
	print('Adding spectra')
	#add the components up
	a, b = add_specs(component_spectra)
	#plot the total spectra
	plt.plot(a, b, 'r--', linewidth=5, label='Total Flux')
	
	#stuff for graph to make titles, labels etc.
	plt.minorticks_on()
	if gap_start!=gap_end:
		plt.title('Spectral Energy Distribution of a Star and Dust Disk\nDisk Extends ({0:0.3f}$<$ r$<${1:0.3f}) AU and ({2:0.3f}$<$ r$<${3:0.3f}) AU'.format((start)/1.5E11, gap_start/1.5E11, gap_end/1.5E11, end/1.5E11))
	else:
		plt.title('Spectral Energy Distribution of a Star and Dust Disk\nDisk Extends ({0:0.3f}$<$ r$<${1:0.3f}) AU'.format((start)/1.5E11, end/1.5E11))
	plt.ylabel('Flux (in units of peak stellar flux)')
	plt.xlabel('Wavelength (nm)')
	plt.legend()
	plt.xlim(0,5000)
	print('Showing plot...')
	plt.show()
	