import sys, string
sys.path.append("/home/dk/wirelessdata")
import raiburari
import numpy

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

sampleList = []
sampleList = raiburari.loadSampleList() # Dictionary of Sample Instances
sampleDic = {}
sampleDic = raiburari.loadSampleDic() # Dictionary of Sample Instances

dicA = {}
inf = open(inputfile, 'r')
line = inf.readline()
while line:
	line = string.strip(line)
	words = line.split()
	mac1 = words[0]
	mac2 = words[1]
	
	if (mac1 not in sampleDic) or (mac2 not in sampleDic):
		line = inf.readline()
		continue
	
	simList = []
	if len(words[2:]) == 0:
		average = 0.0
		median = 0.0
	else:
		for sim in words[2:]:
			simList.append(float(sim))
		if len(simList) == 0:
			average = 0.0
			median = 0.0
		else:
			average = numpy.average(simList)
			median = numpy.median(simList)
	if mac1 in dicA:
		dicA[mac1].update({mac2:[average, median, simList]})
	else:
		dicA[mac1] = {mac2:[average, median, simList]}
	line = inf.readline()
inf.close()
print "loaded"

outf = open(outputfile, 'w')
for sample1 in sampleList:
	for sample2 in sorted(sampleList):
		try:
			result = dicA[sample2.hashedmac][sample1.hashedmac]
		except:
			try : result = dicA[sample1.hashedmac][sample2.hashedmac]
			except : continue
		result0 = result[2][:]
		while 0.0 in result[2]: result[2].remove(0.0)
		if sample1.owner == sample2.owner:
			print >> outf, "1 %f %f %s %s %s %s %d(with 0) %d(without 0)" % (result[0], result[1], sample1.owner, sample1.device, sample2.owner, sample2.device, len(result0), len(result[2]))
			#print >> outf, result[2]
		else:
			print >> outf, "0 %f %f %s %s %s %s %d(with 0) %d(without 0)" % (result[0], result[1], sample1.owner, sample1.device, sample2.owner, sample2.device, len(result0), len(result[2]))
			#print >> outf, result[2]
outf.close()




