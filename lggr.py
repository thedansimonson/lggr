"""
Lggr 0.4 (Alpha)
By Dan Simonson
"""
from datetime import datetime, timedelta
import pickle
import sys

print "\n----Welcome to Logr!----"

#recents load here
recents = []
recentFName = "recents.dat"
try:
	recentFile = open(recentFName,"r+")
	recents = pickle.load(recentFile)
	recentFile.close()
	print "Recents: (type number to load)"
except IOError, EOFError:
	print "Recents not found."
	recents = []

#menu
print " q) quit"
for recent, i in zip(recents, range(0,len(recents))):
	print " "+str(i)+") "+str(recent)
print "Type either the filename or the number of a recent."
print "For a new log, type the filename with the extension."

#this is the main user prompt
filename = raw_input()

#check for quit
if filename == "quit" or filename == "q": sys.exit(0)

#check for a recent
try:
	recentIndex = int(filename)
	filename = recents[recentIndex]
except ValueError:
	print "Accepting raw file name"

#at this point, we have a filename
#if we can't load the file, it's a new file 
logFileLoad = "" #the log is stored here while we edit
try:
	logFile = open(filename, "r+")
	logFileLoad = logFile.read()
	logFile.close()
	backupLog = open("backup_"+filename, "w")
	backupLog.write(logFileLoad)
	backupLog.close()
except IOError:
	print "File not found. Opening new file."

#write here incase the system crashes before a save
temp = open("temp_"+filename, "w")

#save file to recents. if it's in there, remove it so 
#it can be bumped up front
if filename in recents: recents.remove(filename)

#update recents
recents.insert(0,filename)	#newest to front of list
if len(recents) >= 10: recents = recents[0:9]
recentFile = open(recentFName, "w")
pickle.dump(recents,recentFile)
recentFile.close()

print "Log title? (leave blank to skip)"
topic = raw_input()

entry = ""
entries = []
#function to format each line of output
outputEntry = lambda whenWhat: datetime.strftime(whenWhat[0],"%H:%M:%S")+\
		": "+whenWhat[1]+"\n\n"
start = datetime.now()
print "Logging is active. Time recorded: " + str(start)

#built-in commands
def goof(lastEntry): return datetime.now() - lastEntry
def taem(lastEntry): print datetime.now()
def todo(lastEntry, *args):
	note = " ".join(args)
	note = "".join("*",note) #bullet that list

#built-in command/result dicts
commands = {"goof": goof,
			"time": taem,
			"todo": todo}


zeroTime = datetime.now()
zeroTime -= zeroTime
results  = {"goof": [zeroTime,zeroTime],
			"time": [],
			"todo": []}

#logging loop
while entry != "done":
	entry = raw_input()

	#handle built-in commands
	cmd = entry.split(" ")
	if cmd[0] in commands:
		#make a list of params (last entry time, and user given params)
		params = [when]
		params.extend(cmd[1:])
		#engage
		results[cmd[0]].append(apply(commands[cmd[0]], params))
	
	#new entry
	when = datetime.now()
	completeEntry = (when,entry)
	entries.append(completeEntry)
	temp.write(outputEntry(completeEntry))
	print "*"
temp.close()

finis = datetime.now()
totalGoofTime = reduce(lambda x,y: x+y, results["goof"])
delta = finis - start
timeWorked = delta - totalGoofTime

print "Logging is done. Time recorded: " + str(finis)
print "Time delta: " + str(delta)
print "Total time goofed: " + str(totalGoofTime)
print "Total time worked: " + str(timeWorked)

#storage
print "Output test"
header = topic+" Log \n Start time: "+str(start)+ \
		"\n End time: "+str(finis)+"\n Time delta: "+str(delta)
header += "\n Time goofed: "+str(totalGoofTime) + "\n Time worked: " +\
		str(timeWorked) + "\n\n"
finalCompleteEntry = header+"".join(map(outputEntry, entries))
finalCompleteEntry = finalCompleteEntry + "----End of "+str(start)+\
		" entry----"
print finalCompleteEntry

logFile = open(filename, "w")
logFile.write("\n\n".join([finalCompleteEntry,logFileLoad])) 
logFile.close()
	
