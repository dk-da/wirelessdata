import sys, string
sys.path.append("/home/dk/wirelessdata")
#import raiburari
#import rpy2.robjects as robjects

"""
sampleList = []
sampleList = raiburari.loadSampleList() # List of Sample Instances

sampleDic = {}
sampleDic = raiburari.loadSampleDic()

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
	print "Usage : python %s inputfile outputfile" % argvs[0]
	quit()

inputfile = argvs[1]
outputfile = argvs[2]

dicA = {}
inf = open(inputfile, 'r')
line = inf.readline()
while line:
	line = string.strip(line)
	words = line.split()
	timestamp = int(words[0])
	mac = words[1]
	if timestamp in dicA:
		dicA[timestamp].update({mac:0})
	else:
		dicA[timestamp] = {mac:0}
	
	
	line = inf.readline()


outf = open(outputfile, 'w')
for time in sorted(dicA.keys()):
	print >> outf, "%d %d" % (time, len(dicA[time].keys()))


