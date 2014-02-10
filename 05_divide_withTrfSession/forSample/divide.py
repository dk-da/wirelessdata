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

START = 0
END = 0
(START, END) = raiburari.getTimeGap(inputfile) # Start and End of UNIX time

sampleList = []
sampleList = raiburari.loadSampleList() # List of Sample Instances

resultDic = {}

for sample in sampleList:
	dicA = {}
	inf = open("/home/dk/mac/"+sample.hashedmac+"/data.txt", "r")
	for line in inf.readlines():
		line = string.strip(line)
		words = line.split()
		timestamp = int(words[0])
		ap = words[1]
		rssi = int(words[2])
		rx_byte = int(words[3])
		tx_byte = int(words[4])
		rx_pkt = int(words[5])
		tx_pkt = int(words[6])
		dicA[timestamp] = [ap, rssi, rx_byte, tx_byte, rx_pkt, tx_pkt]
	inf.close()
	
	resultDic[sample.hashedmac] = []
	preTxByte = 0
	duration = 0
	for time in range(START, END, 60):
		if time in dicA:
			tx_byte = dicA[time][3]
			if tx_byte >= preTxByte:
				duration += 1
				preTxByte = tx_byte
			else:
				if dicA[time][1] == -128: #pass -128 data
					duration += 1
					continue
				else:
					resultDic[sample.hashedmac].append(tx_byte)
					duration = 0
					preTxByte = tx_byte
		else:
			if preTxByte != 0:
				resultDic[sample.hashedmac].append(tx_byte)
				duration = 0
				preTxByte = 0
			else:
				duration = 0
				preTxByte = 0
		
	while 0 in resultDic[sample.hashedmac]: resultDic[sample.hashedmac].remove(0)

import numpy
for sample in sampleList:
	length = len(resultDic[sample.hashedmac])
	average = numpy.average(resultDic[sample.hashedmac])
#	gmean = numpy.gmean(resultDic[sample.hashedmac])
#	hmean = numpy.hmean(resultDic[sample.hashedmac])
	median = numpy.median(resultDic[sample.hashedmac])
	print sample.hashedmac + " " + sample.owner + " " + sample.device + " average:%d"%(average/1000000) +" median:%d"%(median/1000000)+" len:%d"%length
#	for session in resultDic[sample.hashedmac]:
#		print "%d " % session,









