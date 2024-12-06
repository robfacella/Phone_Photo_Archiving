#!/bin/python3
import os
from datetime import date, timezone
import datetime

def NameTimeStampParser(filename):
	timeyWhimey= filename[4:22]
	dddd=timeyWhimey[:8]
	#YYYY-MM-DAY.... do i even want to import datetime at this rate?
	dddd=date.fromisoformat(dddd)
	tsts=timeyWhimey[9:]
	hour=tsts[:2]
	mins=tsts[2:4]
	secs=tsts[4:6]
	mili=tsts[6:9]
	print (f"{filename} was created at this time: {dddd} {hour}:{mins}:{secs}.{mili}")
	# DateTime is kinda busted on loose timestamps, so i might just return all the vars..
	# Photo Taken at 8:34pm Eastern Time showing as 013415467, -5 from UTC checks out
	return
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
