import ftplib
from ftplib import FTP

import os

# Going to be local to YOU
phoneIP='192.168.1.152'
# Probably Arbitrary
port=7871
# Default for FileManager+
username='pc'
# Set to Random, should read in as argument in future
passwort = '398163'

# Where on local File System you want to Backup the Phone to
backupLocation="/media/rob/38B62D40724FA264/phone/PIXEL"

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
	print ( "Items in List " + str(len(filenames)) )
	return filenames
verboseList()

vCD("device")
verboseList()

# Can move multiple Directories at a time.
vCD("DCIM/Camera")
#verboseList()

filenames=getFileList()

#for files in filenames:
#	print ( files )
print ( "now Just print files 0 and 1 ")
print (filenames[0])
print (filenames[1])

print ( "Local dir: " + os.getcwd() )
#os.getcwd()
os.chdir(backupLocation)
print ( "Local dir: " + os.getcwd() )

# Single File Backup
# Write file in binary mode
with open(filenames[0], "wb") as file:
    # Command for Downloading the file "RETR filename"
    ftp.retrbinary(f"RETR {filenames[0]}", file.write)
# Does not preserve Modified Timestamp
# Also seems to Write EVERY time
