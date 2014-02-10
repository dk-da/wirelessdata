import sys, string
sys.path.append("/home/dk/wirelessdata")
import raiburari
#import rpy2.robjects as robjects

"""
aplist = []
aplist = raiburari.loadAPlist() # List of AP strings

macList = []
macList = raiburari.getMacs(inputfile) # List of all macs(hashed) in file

START = 0
END = 0
(START, END) = raiburari.getTimeGap(inputfilename) # Start and End of UNIX time
"""

argvs = sys.argv
argc = len(argvs)
if (argc != 3):
	print "Usage : python %s inputfile outputfolder" % argvs[0]
	quit()

inputfile = argvs[1]
outputfolder = argvs[2]

dicA = {}
dicA = raiburari.convertMatrixFile2HashWithName(inputfile) # dictionary[node1str][node2str] = float value

dDic = {}
durationf = open("/home/dk/wirelessdata/05_divide_withTrfSession/sessionNumbersAndDurations.txt", 'r')
for line in durationf.readlines():
	line = string.strip(line)
	words = line.split()
	mac = words[0]
	nduration = int(words[1])
	duration = int(words[2])
	dDic[mac] = nduration
durationf.close()


sampleList = []
sampleList = raiburari.loadSampleList() # List of Sample Instances

samef = open(outputfolder+"/same.txt", 'w')
difff = open(outputfolder+"/diff.txt", 'w')
for i, sample1 in enumerate(sampleList):
	for sample2 in sampleList[i+1:]:
		sim = dicA[sample1.hashedmac][sample2.hashedmac]
		d1 = dDic[sample1.hashedmac]
		d2 = dDic[sample2.hashedmac]
		d = min(d1,d2)
		
		if sample1.owner == sample2.owner:
			print >> samef, "%s %f %d" % (sample1.owner+sample1.device+sample2.owner+sample2.device, sim, d)
		else:
			print >> difff, "%s %f %d" % (sample1.owner+sample1.device+sample2.owner+sample2.device, sim, d)
samef.close()
difff.close()










