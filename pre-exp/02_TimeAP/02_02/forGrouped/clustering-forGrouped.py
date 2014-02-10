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
	print "Usage : python %s inputMatrixfile output" % argvs[0]
	quit()

inputfile = argvs[1]
outputfile = argvs[2]
outf = open(outputfile, 'w')

dicA = {}
dicA = raiburari.convertMatrixFile2HashWithName(inputfile) # dictionary[node1str][node2str] = float value

sampleList = []
sampleList = raiburari.loadSampleList() # List of Sample Instances

sampleDic = {}
sampleDic = raiburari.loadSampleDic()

macList = sorted(dicA.keys())
macLen = len(macList)

groupDic = {}
clustDic = {}
groupf = open("/home/dk/wirelessdata/markov_withDiag/output/kmeans/kmeans01.txt", 'r')
for line in groupf.readlines():
	line = string.strip(line)
	words = line.split()
	num = int(words[0])
	clust = int(words[1])
	
	mac = macList[num-1]
	groupDic[mac] = clust
	
	if clust in clustDic:
		clustDic[clust].append(mac)
	else:
		clustDic[clust] = []
		clustDic[clust].append(mac)
groupf.close()

resultDic = {}
for clust, l in clustDic.items():
	for mac in l:
		maxmac = ""
		maxscore = 0.0
		for targetmac in l:
			if mac == targetmac : continue
			if dicA[mac][targetmac] > maxscore:
				maxmac = targetmac
				maxscore = dicA[mac][targetmac]
		if maxscore == 0.0 : resultDic[mac] = {"alone":0.0}
		else : resultDic[mac] = {maxmac:maxscore}


clust = {}
c = 1
alonec = 10001
for device1 in sorted(resultDic.keys()):
	device2 = resultDic[device1].keys()[0]
	if device2 == "alone":
		clust[device1] = alonec
		alonec += 1
		continue
	if device1 in clust:
		clust[device2] = clust[device1]
	else:
		if device2 in clust:
			clust[device1] = clust[device2]
		else:
			clust[device1] = c
			clust[device2] = c
			c += 1

reverseclust = {}
for k, v in clust.items():
	if v not in reverseclust:
		reverseclust[v] = []
		reverseclust[v].append(k)
	else:
		reverseclust[v].append(k)
"""
for mac, cl in clust.items():
	if mac in sampleDic:
		print mac, cl, sampleDic[mac].owner, sampleDic[mac].device

for cl, clist in reverseclust.items():
	flag = 0
	for mac in clist:
		if mac in sampleDic:
			flag = 1
	if flag == 1:
		print ""
		print "cluster : "+str(cl), "(num = %d)" % len(clist)
		for sam in clist:
			if sam in sampleDic:
				print sampleDic[sam].owner+"."+sampleDic[sam].device,
		print ""
"""
TP = 0.0
TN = 0.0
FP = 0.0
FN = 0.0
for i, sample1 in enumerate(sampleList):
	for sample2 in sampleList[i+1:]:
		if sample1.owner == sample2.owner:
			if clust[sample1.hashedmac] == clust[sample2.hashedmac]:
				TP += 1.0
			else:
				FN += 1.0
		else:
			if clust[sample1.hashedmac] == clust[sample2.hashedmac]:
				FP += 1.0
			else:
				TN += 1.0
print "TP:%d, TN:%d, FP:%d, FN:%d" % (TP,TN,FP,FN)
A = (TP + TN)/(TP+TN+FP+FN)
P = (TP) / (TP+FP)
R = (TP) / (TP+FN)
F = 2*P*R / (P+R)
print "Accuracy : %f" % A
print "Precision : %f" % P
print "Recall : %f" % R
print "F-measure : %f" % F


#for cl,clist in reverseclust.items():
#	print >> outf, "cluster no.%d (%d nodes)" % (cl, len(clist))
#	for node in clist:
#		try : print >> outf, resultDic[node][ resultDic[node].keys()[0]  ],
#		except : continue
#	print >> outf, ""



#for mac, cl in clust.items():
#	print >> outf, mac, cl


