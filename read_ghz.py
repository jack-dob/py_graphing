#!/Library/Frameworks/Python.framework/Versions/Current/bin//python

if __name__=='__main__':
	import sys, os
	import matplotlib.pyplot as plt
	f =  open(sys.argv[1])

	nums=[]
	for aline in f:
		nums.append(aline.split())
	f.close()
	
	#print(nums)
	plt.plot([x[0] for x in nums], [y[1] for y in nums], 'b-')
	plt.gca().fill_between(range(0,len(nums)), 0, [y[1] for y in nums], facecolor='blue')
	plt.show()
	