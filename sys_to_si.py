#!/Library/Frameworks/Python.framework/Versions/Current/bin//python

def year(sys_time):
	import math
	year_time = sys_time/(2*math.pi) #convert into years
	return(year_time)

def time(sys_time):
	year_time = year(sys_time) #convert into years
	si_time = year_time*365.24*24*60*60 #convert into seconds
	return(si_time)
	
def dist(sys_dist):
	si_dist = 149597870700.0*sys_dist #system is in AU, convert to meters
	return(si_dist)
	
def mass(sys_mass):
	si_mass = 1.989E30*sys_mass #system is in solar masses, convert to Kg
	return(si_mass)