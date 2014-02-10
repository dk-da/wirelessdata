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

dicA = {}
dicA = raiburari.convertMatrixFile2HashWithName(matrixfilename) # dictionary[node1str][node2str] = float value
"""

argvs = sys.argv
argc = len(argvs)
if (argc != 3):
	print "Usage : python %s inputfile outputfolder" % argvs[0]
	quit()

inputfile = argvs[1]
outputfolder = argvs[2]

sampleList = []
sampleList = raiburari.loadSampleList() # List of Sample Instances

dicA = {}
inf = open(inputfile, 'r')
samef = open(outputfolder+"/same.txt",'w')
difff = open(outputfolder+"/diff.txt", 'w')
for line in inf.readlines():
	line = string.strip(line)
	words = line.split(" ")
	truth = int(words[0])
	average = float(words[1])
	median = float(words[2])
	per95 = float(words[3])
	(owner1,device1,owner2,device2) = words[4].split(".")
	mac1 = words[5]
	mac2 = words[6]
	division1 = ""
	division2 = ""
	for sample in sampleList:
		if sample.hashedmac == mac1 : division1 = sample.division
		if sample.hashedmac == mac2 : division2 = sample.division
	if (division1 == "elab") and (division2 == "elab"):
		print >> samef, average, owner1, device1, owner2, device2
	if ((division1 == "elab") and (division2 == "etc")) or (division2 == "elab") and (division1 == "etc"):
		print >> difff, average, owner1, device1, owner2, device2
inf.close()


#1 0.834625 0.992811 1.000000 dk.pc.dk.sp ce8b817766f9b23baef6946f7548767b7df9bedc dbbd31af7e96f037fcb5114ff6a0633799b4b51c
