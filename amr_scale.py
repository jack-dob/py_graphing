#!/Library/Frameworks/Python.framework/Versions/Current/bin//python



def scale_amr_grid(amr_grid, outfname=None):
	cm_per_au = 1.5E13
	f = open(amr_grid, 'r')
	iformat = int(f.readline())
	zero = int(f.readline())
	coord = int(f.readline())
	g_info = int(f.readline())
	incl_x, incl_y, incl_z = map(int, f.readline().split())
	nx, ny, nz = map(int, f.readline().split())
	
	if(incl_x!=0):
		xlist = map(float, f.readline().split())
	if(incl_y!=0):
		ylist = map(float, f.readline().split())
	if(incl_z!=0):
		zlist = map(float, f.readline().split())
	f.close() #have read in everything
	
	print("limits in x: {} {} (AU)".format(xlist[0]/cm_per_au, xlist[-1]/cm_per_au))
	print("limits in y: {} {} (AU)".format(ylist[0]/cm_per_au, ylist[-1]/cm_per_au))
	print("limits in z: {} {} (AU)".format(zlist[0]/cm_per_au, zlist[-1]/cm_per_au))
	scalar = raw_input("Please scaling factor: ")
	scalar = float(scalar)
	
	if(incl_x!=0):
		xlist = [x*scalar for x in xlist]
	if(incl_y!=0):
		ylist = [y*scalar for y in ylist]
	if(incl_z!=0):
		zlist = [z*scalar for z in zlist]
	
	if outfname==None:
		f = sys.stdout
	else:
		f = open(outfname, 'w')
	
	f.write("{}\n".format(iformat))
	f.write("{}\n".format(zero))
	f.write("{}\n".format(coord))
	f.write("{}\n".format(g_info))
	f.write("{} {} {}\n".format(incl_x, incl_y, incl_z))
	f.write("{} {} {}\n".format(nx, ny, nz))
	for x in xlist:
		f.write("{} ".format(x))
	f.write("\n")
	for y in ylist:
		f.write("{} ".format(y))
	f.write("\n")
	for z in zlist:
		f.write("{} ".format(z))
	f.write("\n")
	
	f.close()
	
	
	
	
	
	
	

if __name__=="__main__":
	import sys, os
	
	if len(sys.argv) > 3:
		print("Error, can only scale one amr_grid.inp file at once")
		sys.exit(0)
	
	amr_grid = sys.argv[1]
	if len(sys.argv)==3:
		outfname = sys.argv[-1]
	else:
		outfname=None
		
	scale_amr_grid(amr_grid, outfname)
	