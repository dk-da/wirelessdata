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

dicA = {}
dicA = raiburari.convertMatrixFile2HashWithName(matrixfilename) # dictionary[node1str][node2str] = float value
"""

argvs = sys.argv
argc = len(argvs)
if (argc != 3):
	print "Usage : python %s inputSamplefile outputfile" % argvs[0]
	quit()

inputfile = argvs[1]
outputfile = argvs[2]

sampleList = []
sampleList = raiburari.loadSampleList() # List of Sample Instances

sampleDic = {}
sampleDic = raiburari.loadSampleDic()

dicA = {}
#1 0.366810 dk pc dk sp
inf = open(inputfile, 'r')
for line in inf.readlines():
	line = string.strip(line)
	words = line.split()
	truth = int(words[0])
	score = float(words[1])
	device1 = words[2]+words[3]
	device2 = words[4]+words[5]
	
	if device1 in dicA:
		dicA[device1].update({device2:score})
	else:
		dicA[device1] = {device2:score}
inf.close()

resultDic = {}
for device in dicA.keys():
	maxscore = 0.0
	maxmac = ""
	for k, v in dicA[device].items():
		if device == k : continue
		if maxscore < v:
			maxscore = v
			maxmac = k
	resultDic[device] = {maxmac:1}

clust = {}
outf = open(outputfile, 'w')
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
	
for device, cl in clust.items():
	print >> outf, device, cl







