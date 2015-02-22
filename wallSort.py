import os,sys,Image,imghdr,shutil,datetime

path16 = "oneSix"
path17 = "oneSeven"

def sortWalls(path):
        oneSixPath = os.path.join(os.path.dirname(path), path16)
        oneSevenPath = os.path.join(os.path.dirname(path), path17)
        badPath = os.path.join(os.path.dirname(path), "Bad")
        logFile = os.path.join(os.path.dirname(os.path.realpath(__file__)), datetime.date.today().isoformat() + ".txt")
        logText = ""
	
        for (root,dirs,files) in os.walk(path):
                logText += "-----\n"
                logText += "Going through %s...\n" % root

                exceptions = os.path.join(root,"exceptions")

                if badPath in dirs:
                        dirs.remove(badPath)
                if oneSixPath in dirs:
                	dirs.remove(oneSixPath)
		if oneSevenPath in dirs:
			dirs.remove(oneSevenPath)

                for infile in files:
                        if not os.path.exists(exceptions) or not check(infile,exceptions):
                                ipath = os.path.join(root,infile)
                                fp = open(ipath, "rb")
                                try:
                                        im = Image.open(fp)
                                        im.load()
                                        width = im.size[0]
                                        height = im.size[1]
                                        rat = float(width)/height

					if isValidSize(rat) == 0:
						newPath = oneSixPath
                                        elif isValidSize(rat) == 1:
                                        	newPath = oneSevenPath
                                        else:
                                        	newPath = badPath

                                        logText += "Moving %s to %s; ratio is %f\n" % (infile, newPath, rat)
                                        dst = root.replace(path, newPath)
                                        if not os.path.exists(dst):
                                        	os.makedirs(dst)
                                        fp.close()
                                        try:
                                        	shutil.move(ipath, dst)
                                        except shutil.Error:
                                        	logText += "%s cannot be moved, as it already exists\n" % infile
                                        	pass
                                        except Exception:
                                        	logText += "%s cannot be moved; it may already exist\n" % infile
                                        	pass
                                except IOError:
                                        logText += "%s is not a valid image!\n" % infile
                                        fp.close()
                                        pass
                        elif check(infile, exceptions):
                        	logText += "%s is an exception; ignoring\n" % infile
                        	pass
                
	writeToLog(logText, logFile)

def isValidSize(imageRat):
	if imageRat == 1.6:
		return 0
	elif imageRat >= 1.7 and imageRat < 1.8:
		return 1

	return 2

def check(fname, ename):
        f = file(ename)
        for name in f:
        	if fname == name:
        		return true
        	else:
        		return false

def writeToLog(string, logFile):
	dst = os.path.split(logFile)[0]

	if not os.path.exists(dst):
		os.makedirs(dst)

	f = open(logFile, 'w')
	f.write(string)
	f.flush()
	f.close()

if __name__ == "__main__":
	if len(sys.argv) == 2:
		sortWalls(sys.argv[1])
	else:
		print "Usage: newressies.py [path to wallpaper folder]"
		quit()
