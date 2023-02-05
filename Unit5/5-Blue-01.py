import csv, random, statistics
import matplotlib.pyplot as plt
import matplotlib as mpl
import random
import numpy as np

m = 0
s = 0

def readData(k):
	data = []
	with open("faithful.csv", 'r') as csvfile:
		csvreader = csv.reader(csvfile)
		fields = next(csvreader)
		for split in csvreader:
			data.append([float(split[0]), float(split[1]), 0])
	return data

def getAverageVals(data, k):
	splitData = [[] for i in range(k)]
	for i in data:
		splitData[i[2]] = splitData[i[2]] + [i]
	
	averageVals = [getAverageVal(i) for i in splitData]
	return averageVals

def getAverageVal(data):
	totalVals = [sum([data[i][0] for i in range(len(data))]), sum([data[i][1] for i in range(len(data))])]
	avgVals = [totalVals[0] / len(data), totalVals[1] / len(data)]
	return avgVals

def assignVals(data, groupAverages):
	for i in range(len(data)):
		data[i] = assignVal(data[i], groupAverages)
	return data

def assignVal(data, groupAverages):
	distFromGroups = [0 for i in range(len(groupAverages))]
	for i in range(len(groupAverages)):
		distFromGroups[i] = (data[0] - groupAverages[i][0]) ** 2 + (data[1] - groupAverages[i][1]) ** 2

	min = distFromGroups[0]
	mindex = 0
	for i in range(len(groupAverages)):
		if distFromGroups[i] < min:
			min = distFromGroups[i]
			mindex = i
	data[2] = mindex
	return data
 
def kmeans(data, k):
	groupAverages = getAverageVals(data, k)
	data = assignVals(data, groupAverages)
	return data

def normalizeData(data):
	for i in range(len(data[0]) - 1):
		vals = [j[i] for j in data]
		standardDeviation = statistics.stdev(vals)
		averageVal = sum(vals) / len(vals)
		for j in range(len(data)):
			data[j][i] = (data[j][i] - averageVal) / standardDeviation
	return data

def getAvgs(data):
	total = [0, 0]
	count = 0
	for i in data:
		total[0] += i[0]
		total[1] += i[1]
		count += 1
	return [total[0] / count, total[1] / count]


def plot(data, firstRun = False):
	global m
	global s


	group0 = []
	group1 = []

	for i in data:
		if i[-1] == 0:
			group0.append(i)
		else:
			group1.append(i)

	temp1 = [i[0] for i in data]
	temp2 = [i[1] for i in data]
	norm1 = mpl.colors.Normalize(vmin = min(temp1), vmax = max(temp1))
	norm2 = mpl.colors.Normalize(vmin = min(temp1), vmax = max(temp1))

	Pk = .5
	covariance = .25*np.identity(2)

	x1 = np . linspace( -2.0 , 2.0 , 100 )
	x2 = np . linspace( -2.0 , 2.0 , 101 )

	X1 , X2 = np . meshgrid( x2 , x1 ) # or change indexing


	vf = np.vectorize(f)
	m1 = np . array( [ -1.25 , 1 ] )
	s1 = np . array( [ covariance ] )
	
	m = m1
	s = s1
	Y1 = vf(X1, X2)

	gnk1 = Pk * Y1

	plt.contour(X1, X2, Y1, [ 0.5 ], colors = ['#0000FF'], linewidths = 2)

	m2 = np . array( [ 1.25 , -.75 ] )
	s2 = np . array( [ covariance ] )
	
	m = m2
	s = s2
	Y2 = vf(X1, X2)

	gnk2 = Pk * Y2

	plt.contour(X1, X2, Y2, [ 0.5 ], colors = ['#FF0000'], linewidths = 2)


	redNorm = mpl.colors.Normalize(vmin = min(gnk1.flatten()), vmax = max(gnk1.flatten()))
	blueNorm = mpl.colors.Normalize(vmin = min(gnk2.flatten()), vmax = max(gnk2.flatten()))

	percents = []
    print(len(percents))
	for i in range(len(gnk1)):
		one = redNorm(gnk1[i])
		two = blueNorm(gnk2[i])
		redPercent = one / (one + two)
		bluePercent = two / (one + two)
		percents.append([redPercent, bluePercent])

	for i in range(len(data)):
		xLoc = int((norm1(data[i][0]) + .13) / 1.3 * 100)
		yLoc = int((norm2(data[i][1]) + .13) / 1.3 * 100)
		plt.scatter(data[i][0], data[i][1], c = [[percents[xLoc][0][yLoc], 0, percents[xLoc][1][yLoc]]])

	
	plt.show()
	plt.savefig("5-Blue-01.png")

def f( x1 , x2) :
	global m
	global s
	dx = ( np . array( [ x1 , x2 ] ) - m ) . reshape( -1 , 1 )
	sinv = np . linalg . inv( s )
	p = m . size # number of inputs
	sf = np . power( 2.0 * np . pi , p / 2.0 ) * np . sqrt( np . linalg .det( s ) )
	return 1.0 / sf * np . exp( -0.5 * ( ( dx . T @ sinv ) @ dx ) )

def main():
	k = 2
	steps = 1
	data = readData(k)
	data = normalizeData(data)
	plot(data)
	data = assignVals(data, [[-1, 1], [1, -1]])
	tempData = kmeans([[i[j] for j in range(len(i))] for i in data], k)
	while(tempData != data):
		data = [[i[j] for j in range(len(i))] for i in tempData] #Shallow copy
		tempData = kmeans(tempData, k)
		steps += 1

	print(getAverageVals(tempData, k))
	print(steps)
	#plot(data)

if __name__ == "__main__":
    main()
