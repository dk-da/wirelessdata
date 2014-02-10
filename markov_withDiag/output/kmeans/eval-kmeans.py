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
	print "Usage : python %s cutreefile outputfile" % argvs[0]
	quit()

inputfile = argvs[1]
outputfile = argvs[2]

sampleList = []
sampleList = raiburari.loadSampleList() # List of Sample Instances

sampleDic = {}
sampleDic = raiburari.loadSampleDic()

macList = []
macList = raiburari.getMacs("/home/dk/wirelessdata/01_nogomi/gattai.txt") # List of all macs(hashed) in file

clustDic = {}
inf = open(inputfile, 'r')
outf = open(outputfile, 'w')
for line in inf.readlines():
	line = string.strip(line)
	(num, clust) = line.split()
	mac = macList[int(num)-1]
	
	if clust not in clustDic:
		clustDic[clust] = []
		clustDic[clust].append(mac)
	else:
		clustDic[clust].append(mac)
	
	if mac in sampleDic:
		print >> outf, mac, sampleDic[mac].division, clust, sampleDic[mac].owner, sampleDic[mac].device
inf.close()

for clust in sorted(clustDic.keys()):
	print >> outf, "clust %s has %d items" % (clust, len(clustDic[clust]))
outf.close()


