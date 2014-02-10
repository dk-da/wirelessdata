import sys, string
sys.path.append("/home/dk/wirelessdata")
import raiburari
#import rpy2.robjects as robjects

"""

aplist = []
aplist = raiburari.loadAPlist() # List of AP strings


dicA = {}
dicA = raiburari.convertMatrixFile2HashWithName(matrixfilename) # dictionary[node1str][node2str] = float value
"""

argvs = sys.argv
argc = len(argvs)
if (argc != 3):
	print "Usage : python %s inputfile outputfile" % argvs[0]
	quit()

inputfile = argvs[1]
outputfile = argvs[2]

START = 1370937600
END = 1378886280
NOAP = "00000notconnected"


macList = []
macList = raiburari.getMacs(inputfile)

resultDic = {}

outf = open(outputfile, "w")
for mac in macList:
	dicA = {}
	inf = open("/home/dk/mac/"+mac+"/data.txt", "r")
	for line in inf.readlines():
		line = string.strip(line)
		words = line.split()
		timestamp = int(words[0])
		ap = words[1]
		dicA[timestamp] = ap
	inf.close()
	
	resultDic[mac] = []
	preTime = 0
	preAP = ""
	nsession = 0
	for time in sorted(dicA.keys()):
		if (dicA[time] != preAP):
			nsession += 1
			preTime = time
			preAP = dicA[time]
		elif (time - preTime > 300):
			nsession += 1
			preTime = time
			preAP = dicA[time]
		else:
			preTime = time
			preAP = dicA[time]
	print >> outf, "%s %d" % (mac, nsession)
outf.close()



"""
sampleList = []
sampleList = raiburari.loadSampleList() # List of Sample Instances

for sample in sampleList:
	dicA = {}
	inf = open("/home/dk/mac/"+sample.hashedmac+"/data.txt", "r")
	for line in inf.readlines():
		line = string.strip(line)
		words = line.split()
		timestamp = int(words[0])
		ap = words[1]
		dicA[timestamp] = ap
	inf.close()
	
	resultDic[sample.hashedmac] = []
	preAP = ""
	session = 0
	for time in range(START, END, 60):
		if time in dicA:
			if preAP == dicA[time]:
				session += 1
				preAP = dicA[time]
			else:
				resultDic[sample.hashedmac].append(session)
				session = 0
				preAP = dicA[time]
		else:
			if preAP != NOAP:
				resultDic[sample.hashedmac].append(session)
				session = 0
				preAP = NOAP
			else:
				session = 0
				preAP = NOAP
	while 0 in resultDic[sample.hashedmac]: resultDic[sample.hashedmac].remove(0)

import numpy
for sample in sampleList:
	length = len(resultDic[sample.hashedmac])
	average = numpy.average(resultDic[sample.hashedmac])
#	gmean = numpy.gmean(resultDic[sample.hashedmac])
#	hmean = numpy.hmean(resultDic[sample.hashedmac])
	median = numpy.median(resultDic[sample.hashedmac])
	print sample.hashedmac + " " + sample.owner + " " + sample.device + " average:%d"%average +" median:%d"%median+" len:%d"%length
#	for session in resultDic[sample.hashedmac]:
#		print "%d " % session,
"""









