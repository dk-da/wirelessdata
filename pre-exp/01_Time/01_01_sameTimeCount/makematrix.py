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

progress = 1
total = str(len(dictA))
distDict = {}
for mac1 in dictA.iterkeys():
	for mac2 in dictA.iterkeys():
		if mac1 in distDict:
			distDict[mac1].update({mac2:0})
		else:
			distDict[mac1] = {mac2:0}
		for timestamp in dictA[mac1].iterkeys():
			if timestamp in dictA[mac2]:
				distDict[mac1][mac2] = distDict[mac1][mac2] + 1
	print str(progress)+"/"+total
	progress += 1
dictA.clear()

outf = open(outputfile, "w")
for mac1 in sorted(distDict.keys()):
	line = mac1
	for mac2 in sorted(distDict.keys()):
		line = line + " " + str(distDict[mac1][mac2])
	print >> outf, line
outf.close()




