import sys, string
sys.path.append("/home/dk/wirelessdata")
import raiburari
#import rpy2.robjects as robjects

"""

aplist = []
aplist = raiburari.loadAPlist() # List of AP strings

macList = []
macList = raiburari.getMacs(inputfilename) # List of all macs(hashed) in file

START = 0
END = 0
(START, END) = raiburari.getTimeGap(inputfilename) # Start and End of UNIX time

"""

argvs = sys.argv
argc = len(argvs)
if (argc != 3):
	print "Usage : python %s inputfile outputfile" % argvs[0]
	quit()

inputfile = argvs[1]
outputfile = argvs[2]

dicA = {}
dicA = raiburari.convertMatrixFile2HashWithName(inputfile) # dictionary[node1str][node2str] = float value

sampleList = []
sampleList = raiburari.loadSampleList() # List of Sample Instances

outf = open(outputfile, 'w')
for i, sample1 in enumerate(sampleList):
	for sample2 in sampleList:
#	for sample2 in sampleList[i+1:]:
		try:
			result = dicA[sample1.hashedmac][sample2.hashedmac]
		except:
			continue
		if sample1.owner == sample2.owner:
			print >> outf, "1 %f %s %s %s %s" % (result, sample1.owner, sample1.device, sample2.owner, sample2.device)
		else:
			print >> outf, "0 %f %s %s %s %s" % (result, sample1.owner, sample1.device, sample2.owner, sample2.device)
outf.close()




