#!/bin/python3
import os
from datetime import date, timezone
import datetime
from enum import Enum
import shutil

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
	tsts=timeyWhimey[9:]
	hour=tsts[:2]
	mins=tsts[2:4]
	secs=tsts[4:6]
	mili=tsts[6:9]
	#print (f"{filename} was created on [ {Month(int(month)).name} {day}, {year} ] at [ {hour}:{mins}:{secs}.{mili} ] (UTC)")
	# Photo Taken at 8:34pm Eastern Time showing as 013415467, -5 from UTC checks out
	return (year, month, day, hour, mins, secs, mili)
def Get_VerboseFilelist(filelist):
	# FILE, YEAR, MONTH, DAY, HOUR, MINUTE, SECOND, MILISECOND
	verboseFilelist = []
	for file in filelist :
		year, month, day, hour, mins, secs, mili = NameTimeStampParser(file)
		verboseFilelist.append([file, year, month, day, hour, mins, secs, mili])
	return (verboseFilelist)
def Group_by_Element (filelist, elementID):
	uniqElements = []
	for file in filelist :
		if file[elementID] not in uniqElements :
			uniqElements.append(file[elementID])
	uniqElements.sort()
	# Debug Message
	#print (f"Found files from these unique elements: {uniqElements}")
	YearBook = []
	for year in uniqElements :
		thisYear = []
		for file in filelist :
			if file[elementID] == year :
				thisYear.append(file)
		YearBook.append(thisYear)
	# Array Nesting is [Year][VerboseFile][ElementOfFile]
	#print (f"From {YearBook[0][1][1]} There are {len(YearBook[0])} entries.")
	i = 0
	for year in uniqElements:
		# Debug Iteration
		#print (f"From {year} There are {len(YearBook[i])} entries.")
		i += 1
	return ( YearBook )
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
def CopyToTree(filename, src, dst):
	print (f"Copying '{filename}' from '{src}' to '{dst}'.")
	shutil.copy2(f"{src}{filename}", f"{dst}{filename}")
def Main_Func():
	TestDir = "/media/rob/38B62D40724FA264/phone/PIXEL/"
	SourceFiles = FilesInDir(TestDir)
	TargetedFiles = OnlyMatch_PXL( SourceFiles )
	VTFiles = Get_VerboseFilelist(TargetedFiles)
	# Group by Year
	ByYear = Group_by_Element ( VTFiles, 1 )
	# Group by Month, ByYear
	NestMonths = []
	for Year in ByYear :
		thisMonths = Group_by_Element ( Year, 2 )
		NestMonths.append(thisMonths)
	# Group by Day, ByMonth, ByYear
	NestDays = []
	YearCount = 0
	TaskCounter = 0
	justFileName = ""
	for Year in ByYear :
		disYear = Year[0][1]
		print (f"{disYear} had files found from {len(NestMonths[YearCount])} Months.")
		MonthCount = 0
		for month in NestMonths[YearCount] :
			disMonth = int(month[1][2])
			theseDays = Group_by_Element( month, 3 )
			NestDays.append(theseDays)
			print (f"{Month(disMonth).name} had files found from {len(theseDays)} days:")
			#print (f"{len(month)} month dirs")

			for thisDay in theseDays:
				disDay = thisDay[0][3]
				print ( f"{disDay}:" )
				backupLocTree = f"/media/rob/38B62D40724FA264/phone/SomeBackupDir/{disYear}/{disMonth}/{disDay}/"
				print ( f"{backupLocTree}")
				os.makedirs(backupLocTree, exist_ok=True)
				for file in thisDay :
					# file is verbose, [0] is filename
					print (f"{TaskCounter} of {len(VTFiles)} -- {file[0]}")
					justFileName = file[0]
					CopyToTree(justFileName, TestDir, backupLocTree)
					TaskCounter += 1
				print ( f"" )
			MonthCount += 1
		#theseDays = Group_by_Element ( month[1], 3 )
		YearCount += 1
	#print (f"{len(NestMonths[1])} nestMonths is - Master Yoda, probably")
Main_Func()
