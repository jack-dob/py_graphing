#!/Library/Frameworks/Python.framework/Versions/Current/bin//python


if __name__=="__main__":
	import sys, os
	import numpy as np
	from readss import unpackxdr
	
	#assume all files are ss files, output to terminal
	for arg in sys.argv[1:]:
		print("file:", arg) #tell filename
		data = unpackxdr(arg)
		print("total mass:", np.sum([plist[0] for plist in data[0]]))