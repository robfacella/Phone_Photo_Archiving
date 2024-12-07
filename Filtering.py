#!/bin/python3
import os
from datetime import date, timezone
import datetime
from enum import Enum

class Month(Enum):
	JAN = 1
	FEB = 2
	MAR = 3
	APR = 4
	MAY = 5
	JUN = 6
	JUL = 7
	AUG = 8
	SEP = 9
	OCT = 10
	NOV = 11
	DEC = 12
def NameTimeStampParser(filename):
	timeyWhimey= filename[4:22]
	dddd=timeyWhimey[:8]
	#YYYY-MM-DAY.... do i even want to import datetime at this rate?
	year=dddd[:4]
	month=dddd[4:6]
	day=dddd[6:8]
	#dddd=date.fromisoformat(dddd)
	tsts=timeyWhimey[9:]
	hour=tsts[:2]
	mins=tsts[2:4]
	secs=tsts[4:6]
	mili=tsts[6:9]
	print (f"{filename} was created on [ {Month(int(month)).name} {day}, {year} ] at [ {hour}:{mins}:{secs}.{mili} ] (UTC)")
	# DateTime is kinda busted on loose timestamps, so i might just return all the vars..
	# Photo Taken at 8:34pm Eastern Time showing as 013415467, -5 from UTC checks out
	return (year, month, day, hour, mins, secs, mili)
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
	years23=0
	for file in OnlyMatch_PXL( SourceFiles ) :
		year, month, day, hour, mins, secs, mili = NameTimeStampParser(file)
		if year == "2023" :
			years23 = years23 + 1
			print (f"{Month(int(month)).name} {file}")
	print (f"{years23} of the files were from 2023")
Main_Func()
