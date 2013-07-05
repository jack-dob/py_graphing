#!/Library/Frameworks/Python.framework/Versions/Current/bin//python

class Star:
	def __init__(self, data):
		if len(data)!=13:
			print(len(data))
			print(data)
			print("Error: in STAR Not enough data points, just use empty entries if needed")
			return
		#print(data)
		self.name = conv(str, data[0])
		self.magnitude_v = conv(float, data[1])
		self.magnitude_i = conv(float, data[2])
		self.magnitude_j = conv(float, data[3])
		self.magnitude_h = conv(float, data[4])
		self.magnitude_k = conv(float, data[5])
		self.distance = conv(float, data[6])
		self.metallicity = conv(float, data[7])
		self.mass = conv(float, data[8])
		self.radius = conv(float, data[9])
		self.spec_type = conv(str, data[10])
		self.age = conv(float, data[11])
		self.teff = conv(float, data[12])

class Exo:
	def __init__(self, data):
		if len(data)<30:
			print(len(data))
			print("Error: in EXO Not enough data points, just use empty entries if needed")
			return
		#print(data)
		self.name = conv(str, data[0])
		self.mass = conv(float, data[1]) #in jupiter masses
		self.radius = conv(float, data[2])
		self.period = conv(float, data[3])
		self.axis = conv(float, data[4]) #semi major axis
		self.eccentricity = conv(float, data[5])
		self.inclination = conv(float, data[6])
		self.angular_distance = conv(float, data[7])
		self.publication_status = conv(str, data[8])
		self.discovered = conv(float, data[9])
		self.updated = conv(str, data[10])
		self.omega = conv(float, data[11])
		self.tperi = conv(float, data[12])
		self.detection_type = conv(str, data[13])
		self.molecules = conv(str, data[14])
		self.ra = conv(str, data[15])
		self.dec = conv(str, data[16])
		self.star = Star(data[17:])
	
def conv(type, value):
	if value=='':
		return(None)
	else:
		return(type(value))

def read_exo_csv(filename):
	f = open(filename, 'r')
	eps = []
	f.readline()
	for aline in f:
		#print(aline)
		aline = aline.strip()
		aline = aline.split('"')
		#print(len(aline))
		if(len(aline)!=1):
			aline = fix_quotes(aline)
		aline = ''.join(aline)
		aline = aline.split(',')
		#print(aline)
		eps.append(Exo(aline))
		#sys.exit(0) #for testing
	return(eps)

def fix_quotes(aline):
	if ((len(aline)%2)==0):
		print("Warning, could not fix quotes properly")
	for i in xrange(0, len(aline)):
		if((i%2)==1): #all the odd numbered ones
			aline[i] = remove_token(',', aline[i])
	return(aline)

def remove_token(token, string):
	return(''.join(string.split(token)))


def filter_sma(exoplanets, min, max):
	f_list = []
	for exo in exoplanets:
		if(min < exo.axis < max):
			f_list.append(exo)
	return(f_list)

def filter_mass(exoplanets, min, max):
	f_list = []
	for exo in exoplanets:
		if exo.mass!=None:
			if(min < exo.mass < max):
				f_list.append(exo)
	return(f_list)

def average(data):
	sum=0.0
	N = 0
	for dat in data:
		if dat != None:
			sum += dat
			N+=1
	return(sum/N)

def plot_bins(data_list, n_bins):
	import numpy as np
	import matplotlib.pyplot as plt
	import matplotlib.figure as fig
	#max = data_list.max()
	#min = data_list.min()
	#dx = float(max - min)/n_bins
	
	n, bins, patches = plt.hist(data_list, bins=n_bins)
	plt.show()



if __name__=="__main__":
	import sys, os, math
	
	filename = sys.argv[1]
	
	exoplanets = read_exo_csv(filename)
	print(len(exoplanets))
	sma_list = filter_sma(exoplanets, 1.5, 10)
	print(len(sma_list))
	#mass_list = filter_mass(exoplanets, 0.8, 3)
	mass_list = filter_mass(sma_list, 0.8, 5)
	print(len(mass_list))
	print(average([exo.eccentricity for exo in mass_list]))
	plot_bins([exo.eccentricity for exo in mass_list if exo.eccentricity != None], 30)
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	