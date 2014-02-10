import sys, string
import numpy

"""
sys.path.append("/home/dk/wirelessdata")
import raiburari

sampleList = []
sampleList = raiburari.loadSampleList() # List of Sample Instances

aplist = []
aplist = raiburari.loadAPlist() # List of AP strings

macList = []
macList = raiburari.getMacs(inputfilename) # List of all macs(hashed) in file

START = 0
END = 0
(START, END) = raiburari.getTimeGap(inputfilename) # Start and End of UNIX time

dicA = {}
dicA = raiburari.convertMatrixFile2HashWithName(matrixfilename) # dictionary[node1str][node2str] = float value
"""

argvs = sys.argv
argc = len(argvs)
if (argc != 3):
	print "Usage : python %s inputVectorFile outputMatrixFile" % argvs[0]
	quit()

inputfile = argvs[1]
outputfile = argvs[2]

inf = open(inputfile, 'r')

progress = 0
dicA = {}
line = inf.readline()
while line:
	line = string.strip(line)
	words = line.split()
	score = float(words[0])
	mac1 = words[1]
	mac2 = words[2]
	
	if mac1 in dicA:
		dicA[mac1].update({mac2:score})
	else:
		dicA[mac1] = {mac2:score}
	line = inf.readline()
inf.close()

macList = sorted(dicA.keys())
macList.append(sorted(dicA[macList[0]].keys())[-1]) #append last mac
macList = sorted(macList)
macLen = len(macList)
print "# of macs : %d" % macLen

outf = open(outputfile, 'w')
for i,mac1 in enumerate(macList):
	print >> outf, mac1,
	for mac2 in macList:
		if mac1 == mac2:
			print >> outf, " %f"%(1.0),
		elif mac1 not in dicA:
			print >> outf, " %f"%dicA[mac2][mac1],
		else:
			if mac2 in dicA[mac1]:
				print >> outf, " %f"%dicA[mac1][mac2],
			else:
				print >> outf, " %f"%dicA[mac2][mac1],
	print >> outf, ""
	print "%d / %d completed" % (i+1, macLen)
outf.close()














