import sys,string

argvs = sys.argv
argc = len(argvs)
if (argc != 3):
	print "Usage : python %s inputmatrixfile outputmatrixfile" % argvs[0]
	quit()

inputfile = argvs[1]
outputfile = argvs[2]

inf = open(inputfile, "r")
outf = open(outputfile, "w")
line = inf.readline()
while line:
	line = string.strip(line)
	words = line.split()
	
	rline = ""
	for word in words:
		value = float(word)
		if value == 0.0:
			ivalue = 999.0
		else:
			ivalue = 1/value
		rline += str(ivalue)+" "
	rline = string.strip(rline)
	print >> outf, rline
	line = inf.readline()
inf.close()
outf.close()




