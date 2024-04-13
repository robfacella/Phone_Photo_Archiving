import ftplib
from ftplib import FTP

# Going to be local to YOU
phoneIP='192.168.1.152'
# Probably Arbitrary
port=7871
# Default for FileManager+
username='pc'
# Set to Random, should read in as argument in future
passwort = '974316'

# Create an FTP object
ftp = FTP()
#ftp = FTP( phoneIP+':'+ port )
#ftp = FTP( host=phoneIP, user=username, passwd=passwort, acct='', timeout=None, source_address=None, *, encoding='utf-8' )

# Connect to a HOST and PORT
ftp.connect(phoneIP, port)
# Give Login Credentials
ftp.login (user=username, passwd=passwort)
# acct='', timeout=None, source_address=None, *, encoding='utf-8' )

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
	return filenames
verboseList()

vCD("device")
verboseList()

# Can move multiple Directories at a time.
vCD("DCIM/Camera")
#verboseList()

filenames=getFileList()

for files in filenames:
	print ( files )
