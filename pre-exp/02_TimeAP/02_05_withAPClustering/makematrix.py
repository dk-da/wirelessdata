import sys,string

argvs = sys.argv
argc = len(argvs)
if (argc != 3):
	print "Usage : python %s inputfile outputfile" % argvs[0]
	quit()

inputfile = argvs[1]
outputfile = argvs[2]

inf = open(inputfile, "r")
alllines = inf.readlines()
firstline = string.strip(alllines[0])
lastline = string.strip(alllines[-1])
del alllines[:]
START = int(firstline.split()[0])
END = int(lastline.split()[0])
inf.close()
print "start : %d" % START
print "end : %d" % END

maclist = []
inf = open(inputfile, "r")
line = inf.readline()
while line:
	line = string.strip(line)
	words = line.split()
	
	timestamp = words[0]
	mac = words[1]
	ap = words[3]
	
	if mac not in maclist:
		maclist.append(mac)
	
	line = inf.readline()
inf.close()
print "file loading completed"

maclist = sorted(maclist)
print "# of macs : %d" % len(maclist)

def loadAPlist():
	aplist = []
	aplistf = open("/home/dk/wirelessdata/aplist.txt", "r")
	for line in aplistf.readlines():
		line = string.strip(line)
		aplist.append(line)
	aplist = sorted(aplist)
	return aplist

aplist = loadAPlist()

APdic = {}
apf = open("/home/dk/wirelessdata/02_apclustering/tpmatrix.txt", "r")
i = 0
line = apf.readline()
while line:
	line = string.strip(line)
	words = line.split()
	for j in range(0, len(words)):
		if aplist[i] in APdic:
			APdic[ aplist[i] ].update( {aplist[j] : float(words[j])} )
		else:
			APdic[ aplist[i] ] = { aplist[j] : float(words[j]) }
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
total = len(maclist)
distDict = {}
for mac1 in maclist:
	mac1dic = loadMac(mac1)
	for mac2 in maclist:
		mac2dic = loadMac(mac2)
		if mac1 in distDict:
			distDict[mac1].update({mac2:1})
		else:
			distDict[mac1] = {mac2:1}
		sameTime = 0
		bunbo = 0.0
		for timestamp in mac1dic.keys():
			if timestamp in mac2dic:
				sameTime += 1
				if mac1dic[timestamp] == mac2dic[timestamp]:
					bunbo += 1.0
				else:
					bunbo += APdic[mac1dic[timestamp]][mac2dic[timestamp]]
		distDict[mac1][mac2] = bunbo / float( len(mac1dic.keys()) + len(mac2dic.keys()) - sameTime )
	i += 1
	print "%d / %d completed" % (i, total)

outf = open(outputfile, "w")
for mac1 in sorted(distDict.keys()):
	line = mac1
	for mac2 in sorted(distDict.keys()):
		line = line + " %f"%(distDict[mac1][mac2])
	print >> outf, line
outf.close()



