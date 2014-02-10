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

NOAP = "00000notconnected"

macList = []
macList = raiburari.getMacs(inputfile)
macLen = len(macList)

dicA = {}
for mac in macList:
	dicA[mac] = {}
	inf = open("/home/dk/mac/"+mac+"/data2.txt", "r")
	for line in inf.readlines():
		line = string.strip(line)
		words = line.split()
		timestamp = int(words[0])
		ap = words[1]
		weight = float(words[3])
		
		dicA[mac][timestamp] = [ap, weight]
	inf.close()

progress = 0
distDict = {}
for mac1 in dicA.iterkeys():
	for mac2 in dicA.iterkeys():
		if mac1 in distDict:
			distDict[mac1].update({mac2:0.0})
		else:
			distDict[mac1] = {mac2:0.0}
		sameTime = 0
		for timestamp in dicA[mac1].iterkeys():
			if timestamp in dicA[mac2]:
				sameTime += 1
				if dicA[mac1][timestamp][0] == dicA[mac2][timestamp][0]: #if same AP
					distDict[mac1][mac2] += dicA[mac1][timestamp][1] * dicA[mac2][timestamp][1]
		distDict[mac1][mac2] = float(distDict[mac1][mac2]) / float( len(dicA[mac1].keys()) + len(dicA[mac2].keys()) - sameTime )
	progress += 1
	print "%d / %d completed" % (progress, macLen)
dicA.clear()

outf = open(outputfile, "w")
for mac1 in sorted(distDict.keys()):
	line = mac1
	for mac2 in sorted(distDict.keys()):
		line = line + " " + str(distDict[mac1][mac2])
	print >> outf, line
outf.close()




