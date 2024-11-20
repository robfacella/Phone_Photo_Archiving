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
global Client_Dir
global FTP_Dir
global FTP_IP
global FTP_Port
global FTP_User
global FTP_Pass

# Read in Config(s)
def readFile(filename):
	file = open(filename)
	lines = file.readlines()
	file.close()
	return lines

config = readFile("Config.txt")
def WipeConfigVars():
	# Clear Vars and/or instantiate.
	# I should try to normalize Directory Language choice
	Client_Dir = str("")
	FTP_Dir = ""
	FTP_IP = ""
	FTP_Port = 0
	FTP_User = ""
	FTP_Pass = ""

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
Client_Dir=config[0]
# Going to be local to YOU
FTP_IP=config[2]
FTP_Dir=config[1]
# Probably Arbitrary
FTP_Port=int(config[3])
# Default for FileManager+
FTP_User=config[4]
########################################################
# Set to Random, should read in as argument in future
FTP_Pass = config[5]
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
	FTP_Pass = sys.argv[1]

##############################################################
# Create an FTP object
ftp = FTP()
#ftp = FTP( phoneIP+':'+ port )
#ftp = FTP( host=phoneIP, user=username, passwd=passwort, acct='', timeout=None, source_address=None, *, encoding='utf-8' )

# Connect to a HOST and PORT
ftp.connect(FTP_IP, FTP_Port)
# Give Login Credentials
ftp.login (user=FTP_User, passwd=FTP_Pass)
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
vCD(FTP_Dir)
#verboseList()

# Get List of Filenames from the Location we are backing up; in this case /device/DCIM/Camera
filenames=getFileList()

# Client Side working Directory
#print ( "Local dir: " + os.getcwd() )
os.chdir(Client_Dir)
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
