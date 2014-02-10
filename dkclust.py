import sys
import scipy
#import numpy
import scipy.spatial.distance as distance
from matplotlib.pyplot import show
from scipy.cluster.hierarchy import linkage, dendrogram


def calDist(data):
	dist = distance.pdist(data, metric = 'cityblock')
	return dist

def main(argvs):
	if len(argvs) != 2:
		print >>sys.stderr, "Usage: %s inputdata" % argvs[0]
		sys.exit(1)

	INPUT_DATA = argvs[1]
	data = [[int(d) for d in l.split()] for l in file(INPUT_DATA)]

	dArray = calDist(data);

	#import fastcluster
	#result = fastcluster.ward(dArray)
	result = linkage(dArray, method='complete')

	dendrogram(result)
	show()

if __name__ == "__main__": main(sys.argv)
