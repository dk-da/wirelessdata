import sys, string
import math
import numpy
sys.path.append("/home/dk/wirelessdata")
import raiburari

"""
class Samples:
	def __init__(self, owner, device, mac, hashedmac, division):
		self.owner = owner
		self.device = device
		self.mac = mac 
		self.hashedmac = hashedmac
		self.division = division


dicA = {}
dicA = raiburari.convertMatrixFile2HashWithName(matrixfilename) # dictionary[node1str][node2str] = float value
"""

def loadData(inputfilename):
	dicA = {}
	inf = open(inputfilename, "r")
	line = inf.readline()
	while line:
		line = string.strip(line)
		words = line.split()
		
		timestamp = int(words[0])
		mac = words[1]
		ssid = words[2]
		ap = words[3]
		rssi = int(words[4])
		rx_byte = int(words[5])
		tx_byte = int(words[6])
		rx_pkt = int(words[7])
		tx_pkt = int(words[8])
		
		if mac in dicA:
			dicA[mac].update({timestamp:ap})
		else:
			dicA[mac] = {timestamp:ap}
		
		line = inf.readline()
	print "all data loaded"
	return dicA

def initAdDic(dic):
	for ap1 in aplist:
		for ap2 in aplist:
			if ap1 in dic:
				dic[ap1].update({ap2:0})
			else:
				dic[ap1] = {ap2:0}
	return dic

def getGcor(adDic1, adDic2):
	g1 = []
	g2 = []
	for ap1 in aplist[1:]: # remove NOAP
		for ap2 in aplist[1:]: # remove NOAP
			g1.append(adDic1[ap1][ap2])
			g2.append(adDic2[ap1][ap2])
	return numpy.corrcoef(g1,g2)[0][1]


if __name__ == '__main__':
	argvs = sys.argv
	argc = len(argvs)
	if (argc != 3):
		print "Usage : python %s inputfile outputfile" % argvs[0]
		quit()
	
	inputfile = argvs[1]
	outputfile = argvs[2]
	
	sampleList = []
	sampleList = raiburari.loadSampleList() # List of Sample Instances
	sampleLen = len(sampleList)
	
	macList = []
	macList = raiburari.getMacs(inputfile) # List of all macs(hashed) in file
	macLen = len(macList)
	
	aplist = []
	aplist = raiburari.loadAPlist() # List of AP strings
	apLen = len(aplist)
	
	START = 0
	END = 0
	(START, END) = raiburari.getTimeGap(inputfile) # Start and End of UNIX time
	
	dicA = {}
	dicA = loadData(inputfile)
	
	admList = {}
	for mac in macList:
		admList[mac] = []
		adDic = {}
		adDic = initAdDic(adDic)
		preap = "00000notconnected"
		for time in range(START, END, 60):
			if time in dicA[mac]:
				if preap == dicA[mac][time]:
					adDic[preap][dicA[mac][time]] += 0.5
				else:
					adDic[preap][dicA[mac][time]] += 1
				preap = dicA[mac][time]
			else:
				if preap == "00000notconnected":
					adDic[preap]["00000notconnected"] += 0.5
				else:
					adDic[preap]["00000notconnected"] += 1
				preap = "00000notconnected"
		for ap1 in aplist[1:]: # remove NOAP
			for ap2 in aplist[1:]: # remove NOAP
				admList[mac].append(adDic[ap1][ap2])
	dicA.clear()
	
	resultDic = {}
	progress = 0
	for mac1 in macList:
		resultDic[mac1] = {}
		for mac2 in macList[macList.index(mac1)+1:]:
			resultDic[mac1][mac2] = ""
			gcor = numpy.corrcoef(admList[mac1],admList[mac2])[0][1]
			if math.isnan(gcor) : gcor = 0.0
			line = "%f %s %s" % (gcor, mac1, mac2)
			resultDic[mac1][mac2] = line
		progress += 1
		print "%d/%d completed" % (progress, macLen)
	
	outf = open(outputfile, "w")
	for mac1 in resultDic.keys():
		for mac2 in resultDic[mac1].keys():
			print >> outf, resultDic[mac1][mac2]
	outf.close()


