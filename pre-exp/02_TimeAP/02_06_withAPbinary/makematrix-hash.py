import sys,string
sys.path.append("/home/dk/wirelessdata")
import raiburari
#import rpy2.robjects as robjects

"""
sampleList = []
sampleList = raiburari.loadSampleList() # List of Sample Instances


macList = []
macList = raiburari.getMacs(inputfilename) # List of all macs(hashed) in file

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

aplist = []
aplist = raiburari.loadAPlist() # List of AP strings
aplist.pop(0)

dicA = {}
maclist = []
inf = open(inputfile, "r")
line = inf.readline()
while line:
	line = string.strip(line)
	words = line.split()
	
	timestamp = words[0]
	mac = words[1]
	ap = words[3]
	
	if mac in dicA:
		dicA[mac].update({timestamp:ap})
	else:
		dicA[mac] = {timestamp:ap}
	
	line = inf.readline()
inf.close()
print "file loading completed"

APdic = {}
apf = open("/home/dk/wirelessdata/02_apclustering/tpmatrix_binary.txt", "r") #binary!!
i = 0
line = apf.readline()
while line:
	line = string.strip(line)
	words = line.split()
	for j in range(0, len(words)):
		if aplist[i] in APdic:
			APdic[ aplist[i] ].update( {aplist[j] : int(words[j])} )
		else:
			APdic[ aplist[i] ] = { aplist[j] : int(words[j]) }
	i += 1
	line = apf.readline()
apf.close()

print "i : %d" % i

def loadMac(mac):
	dic = {}
	f = open("/home/dk/mac/"+mac+"/data.txt", "r")
	for line in f.readlines():
		line = string.strip(line)
		words = line.split()
		time = int(words[0])
		if (time < START):
			continue
		if (END < time):
			break
		ap = words[1]
		dic[words[0]] = ap
	return dic

i = 0
total = len(dicA.keys())
distDict = {}
for mac1 in dicA.iterkeys():
	#mac1dic = loadMac(mac1)
	for mac2 in dicA.iterkeys():
		#mac2dic = loadMac(mac2)
		if mac1 in distDict:
			distDict[mac1].update({mac2:0.0})
		else:
			distDict[mac1] = {mac2:0.0}
		sameTime = 0
		bunbo = 0.0
		for timestamp in dicA[mac1].iterkeys():
			if timestamp in dicA[mac2]:
				sameTime += 1
				if dicA[mac1][timestamp] == dicA[mac2][timestamp]:
					bunbo += 1.0
				else:
					bunbo += max(APdic[dicA[mac1][timestamp]][dicA[mac2][timestamp]],APdic[dicA[mac2][timestamp]][dicA[mac1][timestamp]])
		distDict[mac1][mac2] = bunbo / float( len(dicA[mac1].keys()) + len(dicA[mac2].keys()) - sameTime )
	i += 1
	print "%d / %d completed" % (i, total)
dicA.clear()

outf = open(outputfile, "w")
for mac1 in sorted(distDict.keys()):
	line = mac1
	for mac2 in sorted(distDict.keys()):
		line = line + " %f"%(distDict[mac1][mac2])
	print >> outf, line
outf.close()



