#!/Library/Frameworks/Python.framework/Versions/Current/bin//python


def linear_log(i):
	return(math.log(i))
	
def powerlaw_log(i, A, c):
	return(math.log(A)+c*math.log(i))

def linear(i):
	return(i)
	
def powerlaw(i, A, C):
	return((A*i**(C)))

def exp(i, A, C): #exponential function
	return(A*math.exp(i*C))

def plot_function(FUNCTIONS_X, FUNCTIONS_Y, X_args, Y_args, range):
	import matplotlib.pyplot as plt
	if len(FUNCTIONS_X)!=len(FUNCTIONS_Y)!=len(X_args)!=len(Y_args):
		print("Error: Length of x, y function arrays must be the same...")
		return(0)
	for j in xrange(len(FUNCTIONS_X)):
		x=[]
		y=[]
		for i in xrange(*range):
			x.append(FUNCTIONS_X[j](i, *X_args[j]))
			y.append(FUNCTIONS_Y[j](i, *Y_args[j]))
			#print(i, j)
		#plt.plot([math.log(thing) for thing in x], [math.log(thing) for thing in y], label = 'function {}'.format(j))
		plt.plot(x, y, label = 'function {}'.format(j))
		



if __name__=='__main__':
	import matplotlib.pyplot as plt
	from readss import unpackxdr
	from unpickle_chunk import unpickle_chunk
	import sys, os
	import math
	
	#plot_function([linear_log, linear_log], [powerlaw_log, powerlaw_log], [[], []], [[20^(11/6), -11/6], [(20^(11/6)), -5/6]], [1,21,1])
	#plot_function(	[linear, linear, linear, linear],
	#				[powerlaw, powerlaw, powerlaw, powerlaw], 
	#				[[], [], [], []], 
	#				[	[(20.0**(11.0/6.0)), (-11.0/6.0)], 
	#					[(6.0/5.0*(20**(11.0/6.0))), (-5.0/6.0)],
	#					[(((4.0*math.pi)**(1.0/3.0))*(3.0**(2.0/3.0))*(20.0**(11.0/6.0))), (-7.0/6.0)],
	#					[((7.0/6.0)*((4.0*math.pi)**(1.0/3.0))*(3.0**(2.0/3.0))*(20.0**(11.0/6.0))), (-1.0/6.0)]], 
	#				[1,101,1])

	#plt.xlabel("(mass)")
	#plt.ylabel("(function)")
	
	init_val1 = 6E24/1.8E27 #initial value, constant at the front of Ae^(i*C)
	len_scale1 = 1000 #how long/far till next fixed point
	end_val1 = 1.0 #mass of next fixed point
	C1 = (1.0/len_scale1)*math.log(end_val1/init_val1)
	init_val2 = 15.0*6E24/1.8E27 #initial value, constant at the front of Ae^(i*C)
	len_scale2 = 1000 #how long/far till next fixed point
	end_val2 = 1.0 #mass of next fixed point
	C2 = (1.0/len_scale2)*math.log(end_val2/init_val2)
	start = 0
	stop = 1000
	step = 1
	
	plot_function([linear, linear], [exp, exp], [[], []], [[init_val1, C1], [init_val2, C2]], [start,stop,step])
	plt.xlabel("Growth Time (Years)")
	plt.ylabel("Mass ($M_J$)")
	plt.title("Growth Curves to Jupiter Mass")
	#plt.legend()
	plt.show()
	
		