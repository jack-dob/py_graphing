#!/Library/Frameworks/Python.framework/Versions/Current/bin//python

import sys, os

output = sys.argv[-1]

data = []
i=0
for afile in sys.argv[1:-1]:
	data.append([])
	afile = open(afile, 'r')
	afile.readline()
	afile.readline()
	afile.readline()
	for aline in afile:
		data[i].append(map(float, aline.split()))
	afile.close()
	i+=1
out = open(output, 'w')
out.write("\n")
out.write("\n")
out.write("\n") #three ignored lines
print(len(data[0]))
print(data)
for i in xrange(0, len(data[0])):
	out.write("{} {}\n".format(float(data[1][i][0]), float(data[0][i][1])+float(data[1][i][1])))
	
out.close()