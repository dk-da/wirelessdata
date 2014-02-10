import sys ,string
import rpy2.robjects as robjects

argvs = sys.argv
argc = len(argvs)
if (argc != 3):
	print "Usage : python %s inputfolder outputfolder" % argvs[0]
	quit()

inputfolder = argvs[1]
outputfolder = argvs[2]

r = robjects.r

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
	sample = Samples(words[0], words[1], words[2], words[3])
	sampleList.append(sample)
trainingf.close()
print "sample data loaded"


###################################
def gcor(mac1, mac2):
	rscript = """
library(sna)
g1 <- as.matrix(read.table(file="%s/%s.txt", header=F))
g2 <- as.matrix(read.table(file="%s/%s.txt", header=F))
gcor(g1,g2,diag=TRUE)
""" % (inputfolder, mac1, inputfolder, mac2)
	return r(rscript)[0]
###################################




samef = open(outputfolder+"/same.txt", "w")
difff = open(outputfolder+"/diff.txt", "w")
for sample1 in sampleList:
	for sample2 in sampleList[sampleList.index(sample1):]:
		try:
			if (sample1 == sample2):
				continue
			else:
				line = sample1.owner + sample1.device + sample2.owner + sample2.device + " "
				result = gcor(sample1.hashedmac, sample2.hashedmac)
				line += str(result)
				if (sample1.owner == sample2.owner):
					print >> samef, line
				else:
					print >> difff, line
		except:
			continue
samef.close()
difff.close()


