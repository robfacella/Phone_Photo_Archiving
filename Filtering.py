#!/bin/python3
import os
from datetime import date, timezone
import datetime
#import pytz

def NameTimeStampParser(filename):
	timeyWhimey= filename[4:22]
	dddd=timeyWhimey[:8]
	tsts=timeyWhimey[9:]
	#ddts=dddd+tsts
	#timezone = pytz.timezone('America/New_York')
	#NYTime = (datetime.datetime.fromtimestamp(int(ddts), timezone.utc)).astimezone(timezone)

	print (f"{filename} was created at this time: ")
	print (f"    {timeyWhimey}")
	#datetime()
	print (f"{date.fromisoformat(dddd)}")
	print (f"{tsts}")
	#print ( f"{datetime.datetime.fromtimestamp(int(tsts), timezone.utc)}")
	# Photo Taken at 8:34pm Eastern Time showing as 013415467, -5 from UTC checks out
	print (f"Hour: {tsts[:2]} - Min: {tsts[2:4]} - Sec: {tsts[4:6]} - milS: {tsts[6:9]}")
	#print ( f"{NYTime}")
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
