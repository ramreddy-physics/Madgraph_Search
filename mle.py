import numpy as np

folder = np.concatenate((['Events/run_0'+str(i) for i in range(1, 9)], ['Events/run_'+str(i) for i in range(10, 25)]))

#rectified logarithm to avoid precision issues. e (epsilon can be changed depending on required accuracy)

def rect_log(x):
	e = 1.00e-15
	if x < e:
		return np.log(0.5*e/(1-e) + 0.5)

	elif x > 1 -e:
		return np.log(0.5/e + 0.5)

	else:
		return np.log(0.5*x/(1-x) + 0.5)

out = []

Mx = [120 + 20*i for i in range(25)]

for i in range(len(folder)):
	data = np.genfromtxt(folder[i]+'/out.csv', delimiter = ',')

	result = np.sum([rect_log(x[1]) for x in data])
	print(result)
	out.append([Mx[i], result])

#saves the final readable results in results.csv file
np.savetxt('results.csv', out, delimiter = ',')