import sys, string
sys.path.append("/home/dk/wirelessdata")
import raiburari
import numpy

"""
aplist = []
aplist = raiburari.loadAPlist() # List of AP strings


START = 0
END = 0
(START, END) = raiburari.getTimeGap(inputfilename) # Start and End of UNIX time
"""

argvs = sys.argv
argc = len(argvs)
if (argc != 3):
	print "Usage : python %s distMatrixFile kmeansClusteredFile" % argvs[0]
	quit()

matrixfile = argvs[1]
clusterfile = argvs[2]

sampleList = []
sampleList = raiburari.loadSampleList() # List of Sample Instances

sampleDic = {}
sampleDic = raiburari.loadSampleDic()

#macList = []
#macList = raiburari.getMacs(matrixfile) # List of all macs(hashed) in file

dicA = {}
dicA = raiburari.convertMatrixFile2HashWithName(matrixfile) # dictionary[node1str][node2str] = float value

macList = sorted(dicA.keys())
macLen = len(macList)

clustDic = {}
inf = open(clusterfile, 'r')
for line in inf.readlines():
	line = string.strip(line)
	(num, clust) = line.split()
	mac = macList[int(num)-1]
	
	clustDic[mac] = clust
inf.close()

sameList = []
diffList = []
for i, mac1 in enumerate(macList):
	if mac1 not in clustDic : continue
	for mac2 in macList[i+1:]:
		if mac2 not in clustDic : continue
		dist = dicA[mac1][mac2]
		if clustDic[mac1] == clustDic[mac2]:
			sameList.append(dist)
		elif clustDic[mac1] != clustDic[mac2]:
			diffList.append(dist)
sameAverage = numpy.average(sameList)
diffAverage = numpy.average(diffList)

print "same average = %f" % sameAverage
print "diff average = %f" % diffAverage
print (sameAverage - diffAverage)



















