#!/bin/python3
#import os
import glob

'''
TimeStamp Correction is possible in theory.

TimeStamp is baked into the Filename Down to the MiliSecond
'''

DirToCorrect="/media/rob/WinXP/SomeBackupDir/2024/12/11/"
DirToCorrect="/media/rob/WinXP/SomeBackupDir/2024/"

def Get_Files(Directory):
	#print (f"{Directory}")
	files = []
	files = glob.glob( f"{Directory}/**", recursive=True )
	print (f"There are {len(files)} files/folders in {Directory}")
	return files
def FileByType( Filelist, Type ):
	TrimmedList = []
	ext = len(Type)
	print (f"{ext}")
	for file in Filelist:
		fileExt = f"{file[-(ext):]}"
		print (f"{fileExt} vs {Type}")
		if ( str(fileExt) == str(Type) ) :
			print ( True )
			TrimmedList.append(file)
	print (f"{ext}")
	return ( TrimmedList )
def Main():
	TreeWalk = Get_Files(DirToCorrect)
	TreeWalk.sort()
	#print (f"{Months}")
	print (f"Found {len(TreeWalk)} files/folders in the tree")

	JpegFiles = FileByType( TreeWalk, '.jpg' )
	print (f"{len(JpegFiles)} were jpg files.")
	Mp4Files = FileByType( TreeWalk, '.mp4' )
	print (f"{len(JpegFiles)} were mp4 files.")
#	MDFiles = FileByType( TreeWalk, '.md' )
#	print (f"{len(JpegFiles)} were md files.")
	DayDirs = []
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
