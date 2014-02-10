import sys, string
sys.path.append("/home/dk/wirelessdata")
import raiburari
#import rpy2.robjects as robjects

"""
aplist = []
aplist = raiburari.loadAPlist() # List of AP strings

macList = []
macList = raiburari.getMacs(inputfilename) # List of all macs(hashed) in file

START = 0
END = 0
(START, END) = raiburari.getTimeGap(inputfilename) # Start and End of UNIX time

"""

argvs = sys.argv
argc = len(argvs)
if (argc != 2):
	print "Usage : python %s inputSamplefile" % argvs[0]
	quit()

inputfile = argvs[1]

dicA = {}
dicA = raiburari.convertMatrixFile2HashWithName(inputfile) # dictionary[node1str][node2str] = float value

sampleList = []
sampleList = raiburari.loadSampleList() # List of Sample Instances

sampleDic = {}
sampleDic = raiburari.loadSampleDic()

macList = sorted(dicA.keys())
macLen = len(macList)

resultDic = {}
for mac in macList:
	maxmac = ""
	maxscore = 0.0
	for k, v in dicA[mac].items():
		if mac == k : continue
		if v > maxscore:
			maxmac = k
			maxscore = v
	resultDic[mac] = {maxmac:0}

clust = {}
c = 1
for device1 in sorted(resultDic.keys()):
	device2 = resultDic[device1].keys()[0]
	if device1 in clust:
		clust[device2] = clust[device1]
	else:
		if device2 in clust:
			clust[device1] = clust[device2]
		else:
			clust[device1] = c
			clust[device2] = c
			c += 1
	
for mac, cl in clust.items():
	if mac in sampleDic:
		print mac, cl, sampleDic[mac].owner, sampleDic[mac].device







