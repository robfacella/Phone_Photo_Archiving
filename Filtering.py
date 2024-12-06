#!/bin/python3
import os

def NameTimeStampParser(filename):
	timeyWhimey= filename[4:22]
	print (f"{filename} was created at this time: ")
	print (f"    {timeyWhimey}")
def OnlyMatch_PXL(filelist):
	newList = []
	for file in filelist :
		if ( file[:4] == "PXL_" ):
			newList.append(file)
	print (f"There are likely only [{len(newList)}] files/folders which match the PXL_TIMECODE nameing schema")
	return (newList)

def FilesInDir( directory ):
	files = []
	files = os.listdir( directory )
	print (f"There are {len(files)} files/folders in {directory}")
	return files
def Main_Func():
	TestDir = "/media/rob/38B62D40724FA264/phone/PIXEL"
	SourceFiles = FilesInDir(TestDir)
	for file in OnlyMatch_PXL( SourceFiles ) :
		NameTimeStampParser(file)

Main_Func()
