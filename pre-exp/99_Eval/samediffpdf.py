# Output : same, different file

import sys ,string
import math

argvs = sys.argv
argc = len(argvs)
if (argc != 3):
	print "Usage : python %s distmatrixfile outputfolder" % argvs[0]
	quit()

class Samples:
	def __init__(self, owner, device, mac, hashedmac):
		self.owner = owner
		self.device = device
		self.mac = mac
		self.hashedmac = hashedmac

sampleList = []
trainingf = open("/home/dk/wirelessdata/training.txt", "r")
for line in trainingf.readlines():
	line = string.strip(line)
	words = line.split()
	sampleList.append( Samples(words[0], words[1], words[2], words[3]) )
trainingf.close()
print "trainning data loaded"


#### make distArr ######
distArr = []
nameDic = {}

distmatrixfile = argvs[1]
matrixf = open(distmatrixfile, "r")

line = matrixf.readline()
i = 0
while line:
	line = string.strip(line)
	words = line.split()
	nameDic[words[0]] = i
	distArr.append(words[1:])
	i += 1
	line = matrixf.readline()
#######################
matrixf.close()
print "distance array created"

#######################################################
def getDist(hashedmac1, hashedmac2):
	mac1num = nameDic[hashedmac1]
	mac2num = nameDic[hashedmac2]
	return distArr[mac1num][mac2num]
#######################################################


outputfolder = argvs[2]
samefile = outputfolder + "/same.txt"
differentfile = outputfolder + "/diff.txt"
samef = open(samefile, "w")
differentf = open(differentfile, "w")

for sample1 in sampleList:
	for sample2 in sampleList[sampleList.index(sample1):]:
		try:
			if (sample1 == sample2):
				continue
			dist = getDist(sample1.hashedmac, sample2.hashedmac)
			if ( dist ):
				if (sample1.owner == sample2.owner):
					print >> samef, sample1.owner+sample1.device+sample2.owner+sample2.device+" "+str(dist)
				else:
					print >> differentf, sample1.owner+sample1.device+sample2.owner+sample2.device +" " + str(dist)
		except:
			continue

samef.close()
differentf.close()



