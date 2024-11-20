import ftplib
from ftplib import FTP
# for directory navigation:
import os
# for args:
import sys
# Calc Run Time
import time
# starting time
strtTime = time.time()
#######################################################
# Read in Config(s)
def readFile(filename):
	file = open(filename)
	lines = file.readlines()
	file.close()
	return lines

config = readFile("Config.txt")
def wipeConfigVars():
	# Clear Vars and/or instantiate.
	# I should try to normalize Directory Language choice
	'''global localDir=""
	global remoteDir=""'''
	global phoneIP=""
	global port=0
	global username=""
	global password=""

########################################################
#  Split Config Items and Keep only :
#  right of ( equals = sign )
#  Without the Newline Character "\n"
i=0
#print ( "Connecting with these settings: " )
for line in config:
########################################################
	## Should Goto a Switchcase per line and Set Known Fields and/or clear them
	config[i] = (line.split("=")[1]).rstrip()
	# print ( config[i] )
	i = i + 1
########################################################
##############################################################
# Where on local File System you want to Backup the Phone to
backupLocation=config[0]
# Going to be local to YOU
phoneIP=config[2]
# Probably Arbitrary
port=int(config[3])
# Default for FileManager+
username=config[4]
########################################################
# Set to Random, should read in as argument in future
passwort = config[5]
''' expected command line:
py3 backup.py
 ( OR )
py3 backup.py password123

if a password is sent, use it as passwort
'''
# If not argv[1] and not in Config, should be prompting on CLI
if (len(sys.argv) == 2):
	#print ("Passed a Password!!")
	#print ( sys.argv[1] )
	passwort = sys.argv[1]

##############################################################
# Create an FTP object
ftp = FTP()
#ftp = FTP( phoneIP+':'+ port )
#ftp = FTP( host=phoneIP, user=username, passwd=passwort, acct='', timeout=None, source_address=None, *, encoding='utf-8' )

# Connect to a HOST and PORT
ftp.connect(phoneIP, port)
# Give Login Credentials
ftp.login (user=username, passwd=passwort)
# acct='', timeout=None, source_address=None, *, encoding='utf-8' )

# Max Debug Mode
#ftp.set_debuglevel(2)

#ftp.getwelcome()
# There is None for Filemanager Plus

# Print Working Directory and File details within
def verboseList():
	print ( 'PWD: ' + ftp.pwd() )
	print ("retrlines('LIST')")
	ftp.retrlines('LIST')
	print ( " " )

# CD and Print new Working Dir
def vCD(dir):
	print ( "Moving to - " + dir )
	ftp.cwd(dir)
	print ( 'PWD: ' + ftp.pwd() )
	print (" ")

# Get names of all files in Current Working Directory
def getFileList():
	filenames = []
	ftp.retrlines('NLST', filenames.append)
	print ( "Items in List to be Backed up: " + str(len(filenames)) )
	return filenames
def getBackupFileList():
	filenames = []
	filenames = os.listdir(path='.')
	print ( "Items already in backup location: " + str(len(filenames)) )
	return filenames

def downLFile(filename):
	# Write file in binary mode
	with open(filename, "wb") as file:
		# Command for Downloading the file "RETR filename"
		ftp.retrbinary(f"RETR {filename}", file.write)

## List HOME of Android
#vCD("device")
#verboseList()

# Can move multiple Directories at a time.
vCD(config[1])
#verboseList()

# Get List of Filenames from the Location we are backing up; in this case /device/DCIM/Camera
filenames=getFileList()

# Client Side working Directory
#print ( "Local dir: " + os.getcwd() )
os.chdir(backupLocation)
print ( "Local dir: " + os.getcwd() )
# Get Files already Stored
bkupList=getBackupFileList()

# List from Items in Host Location not already Named in Backup Location
reducedList=[x for x in filenames if x not in bkupList]
print ("Backing up " + str(len(reducedList)) + " items from phone, not already found on PC. " )

# Loop and Backup whole of unique files within Phone DCIM Camera
i=0
for file in reducedList:
	i=i+1
	print ("Backing up ["+ str(i) +"]:" + file)
	downLFile(file)
# time ran is TimeNow minus strtTime
runTime = time.time() - strtTime
runTime = round(runTime, 3)
print ("Complete in ~ " + str(runTime) + " ~ seconds.")
