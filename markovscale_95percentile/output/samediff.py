import sys, string
sys.path.append("/home/dk/wirelessdata")
import raiburari
#import rpy2.robjects as robjects

"""
aplist = []
aplist = raiburari.loadAPlist() # List of AP strings

START = 0
END = 0
(START, END) = raiburari.getTimeGap(inputfilename) # Start and End of UNIX time

dicA = {}
dicA = raiburari.convertMatrixFile2HashWithName(matrixfilename) # dictionary[node1str][node2str] = float value
"""

argvs = sys.argv
argc = len(argvs)
if (argc != 3):
	print "Usage : python %s inputfile outputdirectory" % argvs[0]
	quit()

inputfile = argvs[1]
outputdirectory = argvs[2]

sampleList = []
sampleList = raiburari.loadSampleList() # List of Sample Instances


dicA = {}
inf = open(inputfile, "r")
for line in inf.readlines():
	line = string.strip(line)
	words = line.split()
	true = int(words[0])
	gcor = float(words[1])
	namedevice = words[2]
	mac1 = words[3]
	mac2 = words[4]
	if mac1 not in dicA:
		dicA[mac1] = {mac2:gcor}
	else:
		dicA[mac1].update({mac2:gcor})
inf.close()

samef = open(outputdirectory+"/same.txt", "w")
difff = open(outputdirectory+"/diff.txt", "w")
for sample1 in sampleList:
	for sample2 in sampleList[sampleList.index(sample1):]:
		if sample1 == sample2:
			continue
		if sample2.hashedmac in dicA[sample1.hashedmac]:
			value = dicA[sample1.hashedmac][sample2.hashedmac]
		else:
			value = dicA[sample2.hashedmac][sample1.hashedmac]
		if sample1.owner == sample2.owner:
			print >> samef, "%f" % value
		else:
			print >> difff, "%f" % value
samef.close()
difff.close()


