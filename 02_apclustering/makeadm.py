import sys, string
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
NOAP = "00000notconnected"

macDic = {}

inf = open(inputfile, "r")
line = inf.readline()
while line:
	line = string.strip(line)
	words = line.split()
	
	timestamp = int(words[0])
	mac = words[1]
	ap = words[3]
	
	if mac in macDic:
		macDic[mac].update({timestamp:ap})
	else:
		macDic[mac] = {timestamp:ap}
	
	line = inf.readline()
inf.close()
print "file loading completed"

aplen = len(aplist)
print "# of ap : %d" % aplen
maclen = len(macDic)
print "# of mac : %d" % maclen

#### make empty tpDic ######
def initTpDic(dic):
	for ap1 in aplist:
		for ap2 in aplist:
			if ap1 in dic:
				dic[ap1].update({ap2:0})
			else:
				dic[ap1] = {ap2:0}
	return dic
############################


index = 0
tpDic = {}
tpDic = initTpDic(tpDic)
for mac in macDic.iterkeys():
	preap = NOAP
	for time in range(START, END, 60):
		if time in macDic[mac]:
			tpDic[preap][macDic[mac][time]] += 1
			preap = macDic[mac][time]
		else:
			tpDic[preap][NOAP] += 1
			preap = NOAP
	index += 1	
	print "%d/%d completed"%(index, maclen)
macDic.clear()

outf = open(outputfile, "w")
for ap1 in aplist:
	line = ""
	for ap2 in aplist:
		line = line + str(tpDic[ap1][ap2]) + " "
	line = string.strip(line)
	print >> outf, line
outf.close()




