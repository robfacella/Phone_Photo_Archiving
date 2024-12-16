from subprocess import PIPE, run

command = ['whoami']
result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)

#print (result.returncode, result.stdout, result.stderr)
iam = result.stdout
iam = iam.strip()

if iam != 'root' :
	print (f"Hello, {iam}! You are not root")
if iam == 'root' :
	print (f"Welcome home, {iam},")
