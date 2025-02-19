#!/bin/python3
#import os
import glob
import os
import datetime
from datetime import timedelta
import subprocess
import errno
import SpaceCadet
'''
TimeStamp Correction is possible in theory.

TimeStamp is baked into the Filename Down to the MiliSecond
'''

DirToCorrect="/media/rob/WinXP/SomeBackupDir/2024/12/11/"
DirToCorrect="/media/rob/WinXP/SomeBackupDir/2024/"
DirToCorrect="/media/kali/WinXP/SomeBackupDir/2024/"

def TimeWarp(Date, Time):
	try:
		# Set Clock
		SpaceCadet.RunSP("ls /etc/fonts")
		# Doesn't Crash out without root
		SpaceCadet.RunSP("mkdir /etc/FooBar")
		# Going to need to store and process for root/sudo
		SpaceCadet.RunSP("whoami")
	except IOError as e:
		if e[0] == errno.EPERM:
			sys.exit("Become ROOT first young Chronomancer.")

def Run_ShellScript( RunScript ):
	ScriptWords = RunScript.split(" ")
	print (f"{ScriptWords}")
	if len(ScriptWords) > 1:
		print ( "With Args:" )
		subprocess.run(RunScript, shell=True)
	else:
		print ( "Without Args:" )
		subprocess.run(RunScript, shell=True)

def Get_PXL_DateTime(File):
	print (f"{File}")
	noPath = File.split('/')
	print (f"{noPath[-1]}")
	undrSpl = noPath[-1].split('_')
	fDate = undrSpl[1]
	fTime = undrSpl[2].split('.')[0]
	print (f"{fDate} {fTime} UTC")
	return ( fDate, fTime )
def Split_DateTimes(TheDate, TheTime):
	year = TheDate[:4]
	mont = TheDate[4:6]
	day = TheDate[6:8]
	hr = TheTime[:2]
	mn = TheTime[2:4]
	sx = TheTime[4:6]
	ml = TheTime[6:9]
	#print (f'{hr}:{mn}:{sx}.{ml}')
	return (year, mont, day, hr, mn, sx, ml)
def Change_Timezone(Timezone, UTCDate, UTCTime):
	print (f'Adjusting {UTCDate}:{UTCTime}UTC by {Timezone}')
	Year, Month, Day, Hour, Min, Sec, Mili = Split_DateTimes(UTCDate, UTCTime)
	dt = datetime.datetime(int(Year), int(Month), int(Day))
	Hour = int(Hour)+Timezone
	if Hour < 0 :
		Hour = Hour + 24
		# And remove a day. Datetime Timedelta automatically handles months&years too!
		dt = dt - timedelta(1)
		#print ( f'{dt}' )
	Hour = str(Hour)
	if len(Hour) == 1 :
		Hour = '0' + Hour
	print (f"{Hour}")
	dt = str(dt).split(' ')[0]
	#print (f'{dt}')
	dt = dt.split('-')
	Year = dt[0]
	Month = dt[1]
	Day = dt[2]
	print (f'{Year}, {Month}/{Day}')
def Get_Files(Directory):
	#print (f"{Directory}")
	files = []
	files = glob.glob( f"{Directory}/**", recursive=True )
	print (f"There are {len(files)} files/folders in {Directory}")
	return files
def FileByType( Filelist, Type ):
	TrimmedList = []
	ext = len(Type)
	#print (f"{ext}")
	for file in Filelist:
		fileExt = f"{file[-(ext):]}"
		#print (f"{fileExt} vs {Type}")
		if ( str(fileExt) == str(Type) ) :
			#print ( True )
			#print ( f"Adding '{file}' to TrimmedList...")
			TrimmedList.append( file )
		#else:
			#print ( False )
			#print ( f"NOT Adding '{file}' to TrimmedList...")
	#print (f"{ext}")
	#print ( TrimmedList )
	#print ( len(TrimmedList) )
	return ( TrimmedList )
def Main():
	TimeZone = -5
	TreeWalk = Get_Files(DirToCorrect)
	TreeWalk.sort()
	#print (f"{Months}")
	print (f"Found {len(TreeWalk)} files/folders in the tree")

	JpegFiles = FileByType( TreeWalk, '.jpg' )
	print (f"{len(JpegFiles)} were jpg files.")
	Mp4Files = FileByType( TreeWalk, '.mp4' )
	print (f"{len(Mp4Files)} were mp4 files.")
	MDFiles = FileByType( TreeWalk, '.md' )
	print (f"{len(MDFiles)} were md files.")
	## Returned Root Folder but not the 299 Sub Directories... That said, all files are accounted for.
	#DirectoryEndNodes = FileByType( TreeWalk, '/' )
	#print (f"{len(DirectoryEndNodes)} were Directories Nested")

	# Not Recursive
	subfolders = [ f.path for f in os.scandir(DirToCorrect) if f.is_dir() ]
	print (f"{DirToCorrect} had {len(subfolders)} sub-directories.")

	for File in JpegFiles :
		FileDateUTC, FileTimeUTC = Get_PXL_DateTime( File )
		Change_Timezone(TimeZone, FileDateUTC, FileTimeUTC)

	SpaceCadet.RunSP("ls")
	SpaceCadet.RunSP("ls -lah")
	SpaceCadet.RunSP("ls -lah /media/rob")
	SpaceCadet.RunSP("ls -lah MultiConfigs/")
	## Can Probably Run TimeSwapper as a Python-Driven Bash Script?
	## That'd require ROOT Though, so it might be time to move to the dev board..
	#Run_ShellScript( "./TestPyShell.sh" )
	#Run_ShellScript( "./TestPyShell.sh arg1 arg2" )
	Run_ShellScript( "./TestPyShell.sh /media/rob/ arg2" )
	#print ("py3-- Do buffers collide?\n Seems like NO")
	## Run a whoami
	## Save output back to Python

	Run_ShellScript( f"./TestPyShell.sh {File} {FileDateUTC}{FileTimeUTC}UTC" )
	# Just going to need to nest this in a per file loop
	TimeWarp(FileDateUTC, FileTimeUTC)
	#	if root
	#	else
'''	for Month in Months:
		DayDirs.append( Get_Files(Month) )
	DayDirs.sort()
	TotalFiles = []
	for Day in DayDirs:
		#print (f"{Day}")
		ThisDaysFiles = Get_Files(Day)
		print (f"{ThisDaysFiles}")
		for File in ThisDaysFiles:
			TotalFiles.append( File )
	print ( f"Found {len(TotalFiles)} files within the Directory Tree." )
'''
Main()
