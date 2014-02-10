# -*- coding: utf-8 -*-

import sys ,string
#import rpy2.robjects as robjects

class Samples:
	def __init__(self, owner, device, mac, hashedmac, division):
		self.owner = owner
		self.device = device
		self.mac = mac 
		self.hashedmac = hashedmac
		self.division = division

def loadSampleList():
	sampleList = []
	trainingf = open("/home/dk/wirelessdata/training.txt", "r")
	for line in trainingf.readlines():
		line = string.strip(line)
		words = line.split()
		sample = Samples(words[0], words[1], words[2], words[3], words[4])
		sampleList.append(sample)
	trainingf.close()
	print "sample data loaded"
	return sampleList

def loadSampleDic():
	sampleDic = {}
	trainingf = open("/home/dk/wirelessdata/training.txt", "r")
	for line in trainingf.readlines():
		line = string.strip(line)
		words = line.split()
		hashedmac = words[3]
		sample = Samples(words[0], words[1], words[2], words[3], words[4])
		sampleDic[words[3]] = sample
	trainingf.close()
	print "sample data loaded"
	return sampleDic

def loadAPlist():
	aplist = []
	aplist.append("00000notconnected")
	aplistf = open("/home/dk/wirelessdata/aplist.txt", "r")
	for line in aplistf.readlines():
		line = string.strip(line)
		aplist.append(line)
	aplistf.close()
	aplist = sorted(aplist)
	print "AP list loaded. # of AP : %d + NOAP" % (len(aplist)-1)
	return aplist

def getTimeGap(inputfilename):
	inf = open(inputfilename, "r")
	alllines = inf.readlines()
	firstline = string.strip(alllines[0])
	lastline = string.strip(alllines[-1])
	del alllines[:]
	START = int(firstline.split()[0])
	END = int(lastline.split()[0])
	inf.close()
	print "START:%d, END:%d" % (START, END)
	return START, END

def getMacs(inputfilename):
	inf = open(inputfilename, "r")
	macDic = {}
	line = inf.readline()
	while line:
		line = string.strip(line)
		words = line.split()
		mac = words[1]
		if mac not in macDic:
			macDic[mac] = 1
		line = inf.readline()
	inf.close()
	macList = sorted(macDic.keys())
	print "# of macs : %d"%len(macList)
	return macList
		

def convertMatrixFile2HashWithName(inputfilename):
	nameDic = {}
	i = 1
	inf = open(inputfilename, "r")
	line = inf.readline()
	while line:
		line = string.strip(line)
		words = line.split()
		name = words[0]
		
		nameDic[i] = name
		i += 1
		
		line = inf.readline()
	inf.close()
	
	dicA = {}
	inf = open(inputfilename, "r")
	line = inf.readline()
	while line:
		line = string.strip(line)
		words = line.split()
		name = words[0]
		dicA[name] = { nameDic[1] : float(words[1]) }
		for j in range(2, len(nameDic)+1):
			dicA[name].update({ nameDic[j] : float(words[j]) })
		line = inf.readline()
	inf.close()
	
	print "matrix loaded : %d nodes" % (i-1)
	return dicA





