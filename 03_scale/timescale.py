import sys ,string

argvs = sys.argv
argc = len(argvs)
if (argc != 3):
	print "Usage : python %s inputfile outputfile" % argvs[0]
	quit()

inputfile = argvs[1]
outputfile = argvs[2]
inf = open(inputfile, "r")
outf = open(outputfile, "w")

firstline = inf.readline()
for line in inf.readlines() :
	#print string.strip(line)

	try:

		words = line.split()

#	if ( int(words[0] ) == 1369825106 ):
#		print "first time skipped"
#		continue

#	if ( (int(words[0])-1369825141)%60 != 0 ):
#		print words[0]+"is irregular"
#		continue

		words[0] = int(words[0])/10*10
		if ( int(words[0]) < 1372863600 ): # 2013/07/04 00:00:00
			continue
		if ( 1372906800 <= int(words[0]) ): # 2013/07/04 12:00:00
			continue

		if ( len(words) != 9 ):
			print "less than 9 arg"
			continue

		if ( int(words[4]) < -128 ):
			print words[1]+" has low rssi"
			continue

	except:
		print "except"
		continue

	outf.write(line)

outf.close()
