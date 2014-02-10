import sys, string
sys.path.append("/home/dk/wirelessdata")
import raiburari
import math
#import rpy2.robjects as robjects

"""

aplist = []
aplist = raiburari.loadAPlist() # List of AP strings


dicA = {}
dicA = raiburari.convertMatrixFile2HashWithName(matrixfilename) # dictionary[node1str][node2str] = float value
"""

argvs = sys.argv
argc = len(argvs)
if (argc != 2):
	print "Usage : python %s inputfile" % argvs[0]
	quit()

inputfile = argvs[1]

def calCatenary(totalLen, current):
	if totalLen == 1:
		return 1.0
	elif totalLen == 2:
		return 1.0
	else:
		totalLen = totalLen - 1
		return math.sin(math.pi * current / totalLen - math.pi) / (1.5 + 3.0/totalLen) +1

START = 1370937600
END = 1378886280
NOAP = "00000notconnected"

macList = []
macList = raiburari.getMacs(inputfile)
macLen = len(macList)
progress = 0
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
	
	preTime = 0
	preAP = ""
	nsession = 0
	sessionList = []
	for time in sorted(dicA.keys()):
		if (dicA[time] != preAP):
			nsession += 1
			sessionList.append([])
			sessionList[nsession-1].append([time, dicA[time]])
			preTime = time
			preAP = dicA[time]
			dicA[time] = [dicA[time], nsession]
		elif (time - preTime > 300):
			nsession += 1
			sessionList.append([])
			sessionList[nsession-1].append([time, dicA[time]])
			preTime = time
			preAP = dicA[time]
			dicA[time] = [dicA[time], nsession]
		else:
			sessionList[nsession-1].append([time, dicA[time]])
			preTime = time
			preAP = dicA[time]
			dicA[time] = [dicA[time], nsession]
	
	outf = open("/home/dk/mac/"+mac+"/data2.txt", "w")
	for session in sessionList:
		for timeap in session:
			print >> outf, "%d %s %d %f" % (timeap[0], timeap[1], sessionList.index(session), calCatenary(len(session),session.index(timeap)))
	outf.close()
	progress += 1
	print "%d / %d completed" % (progress, macLen)









