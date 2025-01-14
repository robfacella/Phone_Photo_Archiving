import ftplib
from ftplib import FTP
# for directory navigation:
import os
# for args:
import sys
# Calc Run Time
import time
strtTime = time.time() # Start Time (+/-)
global Runtime_Dir
global Client_Dir
global FTP_Dir
global FTP_IP
global FTP_Port
global FTP_User
global FTP_Pass
global ftp

def ToDo():
	print (f"To-Do:")
	print (f"- Sort Config List Alphabetically prior to Iteration")
	print (f"- RandPass dictionary key system..\n\n")
def readFile(filename): # Return File Lines
	file = open(filename)
	lines = file.readlines()
	file.close()
	return lines
def Check_File_Exists(filename):
	if os.path.isfile( filename ): #print(f"The file '{filename}' exists.")
		return ( True )
	else: #print(f"The file '{filename}' does not exist")
		return ( False)
def WipeConfigVars(): # Clear Vars and/or instantiate.
	Set_Client_Dir( str("") )
	Set_FTP_Dir( "" )
	Set_FTP_IP( "" )
	Set_FTP_Port( 21 )
	Set_FTP_User( "" )
	Set_FTP_Pass( None )
def Set_Client_Dir(path):
	global Client_Dir
	Client_Dir = path
def Get_Client_Dir():
	global Client_Dir
	return ( Client_Dir )
def Set_Runtime_Dir(): # Only run this nearto Script Startup
	global Runtime_Dir
	Runtime_Dir = os.getcwd()
def Return_to_Runtime():
	global Runtime_Dir
	os.chdir( Runtime_Dir )
def Set_FTP_Dir(path):
	global FTP_Dir
	FTP_Dir = path
def Get_FTP_Dir():
	global FTP_Dir
	return ( FTP_Dir )
def Set_FTP_IP(ipAddr):
	global FTP_IP
	FTP_IP = ipAddr
def Get_FTP_IP():
	global FTP_IP
	return ( FTP_IP )
def Set_FTP_Port(PortNumber):
	global FTP_Port
	FTP_Port = PortNumber
def Get_FTP_Port():
	global FTP_Port
	return ( FTP_Port )
def Set_FTP_User(seLlama):
	global FTP_User
	FTP_User = seLlama
def Get_FTP_User():
	global FTP_User
	return ( FTP_User )
def Set_FTP_Pass(passwort):
	global FTP_Pass
	FTP_Pass = passwort
def Get_FTP_Pass():
	global FTP_Pass
	return ( FTP_Pass )
def Read_Conf_File(filename): # Scan Config File for Matching Parameters
	config = readFile( filename )
	for line in config:
		line_R = (line.split("=")[1]).rstrip()
		line_L = (line.split("=")[0]) # However; [no]strip should be unnecessary for the LeftHand Arg
		match line_L:
			case "LocalDir":
				Set_Client_Dir( line_R )
			case "RemoteDir":
				Set_FTP_Dir( line_R )
			case "ipAddr":
				Set_FTP_IP( line_R )
			case "port":
				Set_FTP_Port( int( line_R ) )
			case "username":
				Set_FTP_User( line_R )
			case "password":
				Set_FTP_Pass( line_R )
				print ( "DANGER! Password was set from plaintext file! " )
			case _:
				print (f"'{line.rstrip()}' -- Does not match any current config for our Parameters, just letting you know!")
def Try_Connect_Config( ConfFile ):
	global ftp
	WipeConfigVars() # For Sanity, always Wipe Prior to Read-In
	Read_Conf_File( ConfFile )
	print (f"Attempting to connect to {Get_FTP_User()}@{Get_FTP_IP()}....")
	if ( Get_FTP_Pass() != None ):
		print ( f"Password '{Get_FTP_Pass()}' in Conf File, using that..." )
	else:
		if (len(sys.argv) == 2):
			print ( f"Trying command line args[1]'{sys.argv[1]}' as the password....")
			Set_FTP_Pass( sys.argv[1] )
		else: # Prompt user for manual string password entry.
			userInput = input("Enter a password for this server:\n")
			Set_FTP_Pass( userInput )
			# FTP_Lib crashes when the password is wrong
			# ftplib.error_perm: 530 Login incorrect
	# Create an FTP object
	ftp = FTP()
	#ftp = FTP( phoneIP+':'+ port )
	#ftp = FTP( host=phoneIP, user=username, passwd=passwort, acct='', timeout=None, source_address=None, *, encoding='utf-8' )
	# Connect to a HOST and PORT
	ftp.connect(FTP_IP, FTP_Port)
	# Give Login Credentials
	ftp.login (user=FTP_User, passwd=FTP_Pass)
	# acct='', timeout=None, source_address=None, *, encoding='utf-8' ) ''' Max Debug Mode#ftp.set_debuglevel(2)#ftp.getwelcome()#There is None for Filemanager Plus''' # Can move multiple Directories at a time.
	vCD(FTP_Dir)
	#verboseList()
	# Get List of Filenames from the Location we are backing up; in this case /device/DCIM/Camera
	filenames=getFileList()
	# Client Side working Directory #print ( f"Local dir: {os.getcwd()}" )
	os.chdir(Client_Dir)
	print ( f"Local dir: {os.getcwd()}" )
	# Get Files already Stored
	bkupList=getBackupFileList()
	# List from Items in Host Location not already Named in Backup Location
	reducedList=[x for x in filenames if x not in bkupList]
	print (f"Backing up {len(reducedList)} items from phone, not already found on PC." )
	# Loop and Backup whole of unique files within Phone DCIM Camera
	i=0
	for file in reducedList:
		i=i+1
		print (f"Backing up [{i}]:{file}")
		downLFile(file)
	ftp.quit()
def Try_Multi_Conf(MultiPath):
	print ( f"Loop Multi-Conf Directory for '*.txt' files, sorting Alphabetically")
	ConfList = []
	for root, dirs, files in os.walk(MultiPath):
		for file in files:
			ConfList.append(os.path.join(root, file))
	for file in ConfList:
		Return_to_Runtime() # Sanity, always do prior to Iterating on another Config. it's a Lodestone reference point during Teleportation
		fileExt = os.path.splitext(file)[1].lower()
		if ( (fileExt == ".txt") or (fileExt == ".conf") ):
			rFile = file.lstrip("./")
			print ( rFile )
			if ( Check_File_Exists( rFile) ):
				Try_Connect_Config( file.lstrip("./") )
			else:
				print( f"'{rFile}' has ceased to exist, your guess is as good as mine")
		print (f" ")
##############################################################
def Main():
	Set_Runtime_Dir()
	ToDo()
	confFileName="Config.txt"

	if ( Check_File_Exists( confFileName ) ):
		Try_Connect_Config( confFileName )
	else:
		directory_path = "./MultiConfigs"
		if os.path.isdir(directory_path):
			print (f"The directory '{directory_path}' exists.")
			Try_Multi_Conf(directory_path)
		else:
			print (f"The directory '{directory_path}' does not exist.")
			print ( 'Would you like to create it now? [ Y / N ]' )

#######################################################################
# Print Working Directory and File details within
def verboseList():
	print ( f'PWD: {ftp.pwd()}' )
	print ("retrlines('LIST')")
	ftp.retrlines('LIST')
	print ( " " )

# CD and Print new Working Dir
def vCD(dir):
	print ( f"Moving to - {dir}" )
	ftp.cwd(dir)
	print ( f'PWD: {ftp.pwd()}' )
	print (" ")

# Get names of all files in Current Working Directory
def getFileList():
	filenames = []
	ftp.retrlines('NLST', filenames.append)
	print ( f"Items in List to be Backed up: {len(filenames)}" )
	return filenames
def getBackupFileList():
	filenames = []
	filenames = os.listdir(path='.')
	print ( f"Items already in backup location: {len(filenames)}" )
	return filenames

def downLFile(filename):
	# Write file in binary mode
	with open(filename, "wb") as file:
		# Command for Downloading the file "RETR filename"
		ftp.retrbinary(f"RETR {filename}", file.write)

Main()
## List HOME of Android #vCD("device") #verboseList() #########################################################
# Time spent running is equal to TimeNow minus startTime
runTime = time.time() - strtTime
print (f"Complete in ~ {round(runTime, 3)} ~ seconds.")
