import sys,string

argvs = sys.argv
argc = len(argvs)
if (argc != 3):
	print "Usage : python %s inputfile outputfile" % argvs[0]
	quit()

inputfile = argvs[1]
outputfile = argvs[2]

dictA = {}
inf = open(inputfile, "r")
line = inf.readline()
while line:
	line = string.strip(line)
	words = line.split()

	timestamp = words[0]
	mac = words[1]

	if mac in dictA:
		dictA[mac].update({timestamp:1})
	else:
		dictA[mac] = {timestamp:1}
	line = inf.readline()
inf.close()
print "file loading completed"

########################################################
def calDist(mac1, mac2):
	sameTimeCounter = 0.0

	for time in dictA[mac1].iterkeys():
		if time in dictA[mac2]:
			sameTimeCounter += 1.0

	dist = sameTimeCounter / (float(len(dictA[mac1])) + float(len(dictA[mac2])) - sameTimeCounter)
	return dist
########################################################

progress = 1
total = len(dictA)
distDict = {}
for mac1 in dictA.iterkeys():
	for mac2 in dictA.iterkeys():
		if mac1 in distDict:
			distDict[mac1].update({mac2:calDist(mac1,mac2)})
		else:
			distDict[mac1] = {mac2:calDist(mac1,mac2)}
	print "%d / %d" % (progress, total)
	progress += 1
dictA.clear()

outf = open(outputfile, "w")
for mac1 in sorted(distDict.keys()):
	line = mac1
	for mac2 in sorted(distDict.keys()):
		line = line + " " + str(distDict[mac1][mac2])
	print >> outf, line
outf.close()




