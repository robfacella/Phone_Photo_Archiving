from subprocess import PIPE, run
import sys
import SpaceCadet

def QuitIfNotRoot() :
	command = ['whoami']
	result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
	#print (result.returncode, result.stdout, result.stderr)
	iam = result.stdout
	iam = iam.strip()
	if iam != 'root' :
		print (f"Hello, {iam}! You are not root")
		sys.exit("Not Root, exiting...")
	if iam == 'root' :
		print (f"Welcome home, {iam},")
def TimeStatus01() :
	command = ['timedatectl status']
	result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
	print (result.returncode, result.stdout, result.stderr)
	StatusCaptain = result.stdout
	print (f"{StatusCaptain}")
def TimeStatus():
	SpaceCadet.RunSP("timedatectl status")
QuitIfNotRoot()
print ("Did not Quit")
TimeStatus()
