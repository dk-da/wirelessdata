import sys ,string
import rpy2.robjects as robjects

argvs = sys.argv
argc = len(argvs)
if (argc != 4):
	print "Usage : python %s timescale[min] inputfile outputfile" % argvs[0]
	quit()

timescale = int(argvs[1])
inputfile = argvs[2]
outputfile = argvs[3]

r = robjects.r
SAMPLINGRATE = 1 #min

class Samples:
	def __init__(self, owner, device, mac, hashedmac):
		self.owner = owner
		self.device = device
		self.mac = mac 
		self.hashedmac = hashedmac

def loadSampleList():
	sampleList = []
	trainingf = open("/home/dk/wirelessdata/training.txt", "r")
	for line in trainingf.readlines():
		line = string.strip(line)
		words = line.split()
		sample = Samples(words[0], words[1], words[2], words[3])
		sampleList.append(sample)
	trainingf.close()
	print "sample data loaded"
	return sampleList

def loadAPlist():
	aplist = []
	aplist.append("00000notconnected")
	aplistf = open("/home/dk/wirelessdata/aplist.txt", "r")
	for line in aplistf.readlines():
		line = string.strip(line)
		aplist.append(line)
	aplist = sorted(aplist)
	return aplist

def loadData(inputfilename):
	inf = open(inputfilename, "r")
	alllines = inf.readlines()
	firstline = string.strip(alllines[0])
	lastline = string.strip(alllines[-1])
	del alllines[:]
	START = int(firstline.split()[0])
	END = int(lastline.split()[0])
	inf.close()
	START = 1370937600 #2013/6/11 17:00:00
	END = 1378886281 #2013/9/11 16:58:00
	print "START : %d"%START
	print "END : %d"%END
	
	macDic = {}
	inf = open(inputfilename, "r")
	line = inf.readline()
	while line:
		line = string.strip(line)
		words = line.split()
	
		timestamp = int(words[0])
		mac = words[1]
		ap = words[3]
		timestamp = (timestamp/10)*10
	
		if mac in macDic:
			macDic[mac].update({timestamp:ap})
		else:
			macDic[mac] = {timestamp:ap}
		
		line = inf.readline()
	inf.close()
	#aplist.remove("00000notconnected")
	print "input data loaded"
	return START, END, macDic

def initTpDic(dic):
	for ap1 in aplist:
		for ap2 in aplist:
			if ap1 in dic:
				dic[ap1].update({ap2:0})
			else:
				dic[ap1] = {ap2:0}
	return dic

def getGcor(tpDic1, tpDic2):
	tmpf1 = open("/home/dk/tmp/1.txt","w")
	for ap1 in sorted(tpDic1.keys()):
		line = ""
		for ap2 in sorted(tpDic1.keys()):
			line = line + str(tpDic1[ap1][ap2]) + " " 
		line = string.strip(line)
		print >> tmpf1, line
	tmpf1.close()
	tmpf2 = open("/home/dk/tmp/2.txt","w")
	for ap1 in sorted(tpDic2.keys()):
		line = ""
		for ap2 in sorted(tpDic2.keys()):
			line = line + str(tpDic2[ap1][ap2]) + " " 
		line = string.strip(line)
		print >> tmpf2, line
	tmpf2.close()
	rscript = """
library(sna)
g1 <- as.matrix(read.table(file="/home/dk/tmp/1.txt", header=F))
g2 <- as.matrix(read.table(file="/home/dk/tmp/2.txt", header=F))
gcor(g1[2:93,2:93],g2[2:93,2:93], diag=TRUE)
"""
	try:
		return float(r(rscript)[0])
	except:
		return 0.0

def crawl(START, END, scale, mac1dic, mac2dic):
	maxGcor = 0.0
	tpDic1 = {}
	tpDic2 = {}
	for scaletime in range(START, END, scale*60):
		preap1 = "00000notconnected"
		preap2 = "00000notconnected"
		tpDic1 = initTpDic(tpDic1)
		tpDic2 = initTpDic(tpDic2)
		for time in range(scaletime, scaletime + scale*60, SAMPLINGRATE*60):
			if time in mac1dic:
				tpDic1[preap1][mac1dic[time]] += 1
				preap1 = mac1dic[time]
			else:
				tpDic1[preap1]["00000notconnected"] += 1
				preap1 = "00000notconnected"
			if time in mac2dic:
				tpDic2[preap2][mac2dic[time]] += 1
				preap2 = mac2dic[time]
			else:
				tpDic2[preap2]["00000notconnected"] += 1
				preap2 = "00000notconnected"
		gcor = getGcor(tpDic1, tpDic2)
		if (gcor > maxGcor):
			maxGcor = gcor
	return maxGcor

sampleList = loadSampleList()
sampleLen = len(sampleList)
aplist = loadAPlist()
STARTTIME, ENDTIME, macDic = loadData(inputfile)
outf = open(outputfile, "w")
for sample1 in sampleList:
	if sample1.hashedmac not in macDic:
		continue
	for sample2 in sampleList[sampleList.index(sample1):]:
		if sample2.hashedmac not in macDic:
			continue
		if (sample1 == sample2):
			continue
		else:
			maxGcor = crawl(STARTTIME, ENDTIME, timescale, macDic[sample1.hashedmac], macDic[sample2.hashedmac])
			if (sample1.owner == sample2.owner):
				line = "%d %f %s %s %s" % (1, maxGcor, sample1.owner+"."+sample1.device+"."+sample2.owner+"."+sample2.device, sample1.hashedmac, sample2.hashedmac)
				print >> outf, line
			else:
				line = "%d %f %s %s %s" % (0, maxGcor, sample1.owner+"."+sample1.device+"."+sample2.owner+"."+sample2.device, sample1.hashedmac, sample2.hashedmac)
				print >> outf, line
		print "1"
	print "1 of %d completed" % sampleLen
outf.close()



