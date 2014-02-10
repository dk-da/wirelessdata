import sys, string
sys.path.append("/home/dk/wirelessdata")
import raiburari
#import rpy2.robjects as robjects

"""
sampleList = []
sampleList = raiburari.loadSampleList() # List of Sample Instances

sampleDic = {}
sampleDic = raiburari.loadSampleDic()

aplist = []
aplist = raiburari.loadAPlist() # List of AP strings


START = 0
END = 0
(START, END) = raiburari.getTimeGap(inputfilename) # Start and End of UNIX time

dicA = {}
dicA = raiburari.convertMatrixFile2HashWithName(matrixfilename) # dictionary[node1str][node2str] = float value
"""

argvs = sys.argv
argc = len(argvs)
if (argc != 4):
	print "Usage : python %s inputNoGomiFile final_cluster_result.txt outputfile" % argvs[0]
	quit()

inputfile = argvs[1]
clusterfile = argvs[2]
outputfile = argvs[3]

macList = []
macList = raiburari.getMacs(inputfile) # List of all macs(hashed) in file

groupDic = {}
clusterf = open(clusterfile, 'r')
for line in clusterf.readlines():
	line = string.strip(line)
	words = line.split()
	mac = words[0]
	clust = words[1]
	
	groupDic[mac] = clust

dicA = {}
inf = open(inputfile, 'r')
line = inf.readline()
while line:
	line = string.strip(line)
	words = line.split()
	timestamp = int(words[0])
	mac = words[1]
	if timestamp in dicA:
		dicA[timestamp].update({mac:0})
	else:
		dicA[timestamp] = {mac:0}
	
	line = inf.readline()


outf = open(outputfile, 'w')
for time in sorted(dicA.keys()):
	l = []
	for mac in dicA[time].keys():
		if mac in groupDic:
			l.append(groupDic[mac])
		else:
			l.append(mac)
	l = set(l)
	print >> outf, "%d %d" % (time, len(l))


