#!/Library/Frameworks/Python.framework/Versions/Current/bin//python
def frange(start, stop, step):
	list = []
	while start <= stop:
		list.append(start)
		start+=step
	return(list)

def unlog(x):
	return(math.e**x)
	
def neg(x):
	return(-x)

def get_walls_cart(ranges, nums):
	#for cartesian have to have everything rectangular
	
	x_range = ranges[0][1] - ranges[0][0]
	y_range = ranges[1][1] - ranges[1][0]
	x_step = x_range/float(nums[0])
	y_step = y_range/float(nums[1])
	z_step = x_step #has to be cubic
	
	z_min = -0.5*z_step*float(nums[2])
	z_max = 0.5*z_step*float(nums[2])
	x_list = frange(ranges[0][0], ranges[0][1], x_step)
	y_list = frange(ranges[1][0], ranges[1][1], y_step)
	z_list = frange(z_min, z_max, z_step)
	return(x_list, y_list,z_list)
	
	

def get_walls(ranges, nums):
	#for polars assume a log scale
	
	r_log_min = math.log(ranges[0][0])
	r_log_max = math.log(ranges[0][1])
	dr_log = (r_log_max - r_log_min)/float(nums[0])#spacing in log space
	r_log_list = frange(r_log_min, r_log_max, dr_log)
	r_list = map(unlog, r_log_list)
	print(len(r_list))
	
	t_log_min = math.log(0.1) #math.log(ranges[1][0])
	t_log_max = math.log(ranges[1][1])
	dt_log = (t_log_max - t_log_min)/float(nums[1]) #spacing in log space
	t_log_list = frange(t_log_min, t_log_max, dt_log)
	t_list = map(unlog, t_log_list)
	#neg_t_list = map(neg, t_list)
	#t_list+=neg_t_list
	#t_list = sorted(t_list)
	#print("tlist:",t_list)
	
	p_min = ranges[2][0]
	p_max = ranges[2][1]
	dp_log = (p_max - p_min)/float(nums[2]) #spacing
	p_list = frange(p_min, p_max, dp_log)

	return(r_list, t_list, p_list)

def get_dust_density_cart(dopac_file, xlist, ylist, zlist):
	from mk_dkinp import read_dustopac
	name = "dust_density.inp"
	M_in = 1E-20*2.0E33 #1E-8 solar masses in grams
	alpha = M_in/(math.sqrt(3.8) - math.sqrt(0.8)) #factor of 4*pi cancels later
	#print(alpha)
	dust_dat = read_dustopac(dopac_file)
	f = open(name, 'w')
	f.write("1\n") #iformat
	f.write("{}\n".format((len(xlist)-1)*(len(ylist)-1)*(len(zlist)-1))) #number of cells
	f.write("{}\n".format(len(dust_dat)))#number of dust species
	vol_elem = (xlist[1]-xlist[0])*(ylist[1]-ylist[0])*(zlist[1]-zlist[0])
	#print(vol_elem)
	for l in range(0, len(dust_dat)): #loop over each dust species
		a = 0.5*dust_dat[l][2]
		b = 1.5*dust_dat[l][2]
		d_fac = 1.0/(dust_dat[l][0]*(b-a)**(-5/12))
		#print(d_fac, b-a)
		for k in range(0, len(zlist)-1):
			for j in range(0, len(ylist)-1):
				for i in range(0, len(xlist)-1):
					#print(i, j, k)
					r = math.sqrt(xlist[i]*xlist[i] + ylist[j]*ylist[j] + zlist[k]*zlist[k])
					r_inc = math.sqrt(xlist[i+1]*xlist[i+1] + ylist[j+1]*ylist[j+1] + zlist[k+1]*zlist[k+1])
					M_ann = alpha*(math.sqrt(r_inc) - math.sqrt(r)) #mass in this annulus
					#print(M_ann)
					D_cell = d_fac*M_ann/vol_elem #density in this cell
					f.write("{}\n".format(D_cell))
	return()
	

def get_dust_density(dopac_file, xlist, ylist, zlist):
	from mk_dkinp import read_dustopac
	name = "dust_density.inp"
	M_in = 2.0E-7*2E33 #2E-7 solar masses in grams
	dust_dat = read_dustopac(dopac_file)
	print(dust_dat)
	alpha = M_in/(math.sqrt(3.8) - math.sqrt(0.8)) #factor of 4*pi cancels later
	f = open(name, 'w')
	f.write("1\n") #iformat
	f.write("{}\n".format((len(xlist)-1)*(len(ylist)-1)*(len(zlist)-1))) #number of cells
	f.write("{}\n".format(len(dust_dat)))#number of dust species
	for l in range(0, len(dust_dat)):
		for k in range(0, len(zlist)-1):
			dz = abs(zlist[k+1] - zlist[k])
			for j in range(0, len(ylist)-1):
				dy = abs(ylist[j+1] - ylist[j])
				sin_theta = math.sin(ylist[j])
				for i in range(0, len(xlist)-1):
					dx = abs(xlist[i+1] - xlist[i])
					#remember, we are in spherical polars
					t_vol = xlist[i]*xlist[i]*dx*abs(ylist[-1]-ylist[0])*abs(zlist[-1]-zlist[0])
					#approx for total volume in this shell that we have co-ords for
					vol = xlist[i]*xlist[i]*sin_theta*dx*dy*dz #good enough approx for vol of cell
					#area = xlist[i]*dy*dz #surface area of annulus
					M_ann = alpha*(math.sqrt(xlist[i+1]) - math.sqrt(xlist[i])) #mass in this annulus
					D_cell = 0.5*sin_theta*dust_dat[l][0]*M_ann/t_vol #density in this cell
					f.write("{}\n".format(D_cell))
	return()

if __name__=='__main__':
	import os, sys, math
	#This code is used to generate amr_grid.inp files for RADMC3D
	#It is all hard coded for now, remember have to use CGS! angles in RADIANS
	
	cm_per_au = 1.49598E+13
	
	iformat = "1"
	coord = "0" #0 = cart, 100 = sph polar, 200 = cynd polar
	grid_info="0" #no extra info
	incl_x = "1" #r when polars
	incl_y = "1" #theta when polars (down from z axis)
	incl_z = "0" #phi when polars (round from x axis, equatorial plane)
	nx = "100" #number of points
	ny = "100"
	nz = "1"
	#this one is for testing
	#ranges = [ [3.8*cm_per_au, 100.0*cm_per_au], [math.pi/2.0-math.pi/12.0, math.pi/2.0], [0,2.0*math.pi] ]

	ranges = [ [3.8*cm_per_au,100.0*cm_per_au], [3.8*cm_per_au,100.0*cm_per_au], [0.0,0.1] ]
	xlist, ylist, zlist = get_walls_cart(ranges, (nx, ny, nz))
	#print(len(xlist))
	name="amr_grid.inp"
	#if os.path.exists(name):
	#	name = raw_input("file 'amr_grid.inp' exists, enter desired name of file:")
		
	f=open(name, 'w')
	f.write("{}\n".format(iformat))
	f.write("0\n")
	f.write("{}\n".format(coord))
	f.write("{}\n".format(grid_info))
	f.write("{}\t{}\t{}\n".format(incl_x, incl_y, incl_z))
	f.write("{}\t{}\t{}\n".format(len(xlist)-1, len(ylist)-1, len(zlist)-1))
	for item in xlist:
		f.write("{} ".format(item))
	f.write("\n")
	for item in ylist:
		f.write("{} ".format(item))
	f.write("\n")
	for item in zlist:
		f.write("{} ".format(item))
	f.write("\n")
	f.close() #close the file
	
	get_dust_density_cart("dustopac.inp", xlist, ylist, zlist)
	
	
	
	
	
	
	