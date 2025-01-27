#!/bin/python3
import subprocess

def RunSP(Command):
        CommandWords = Command.split(" ")
        print (f"{CommandWords}")
        if len(CommandWords) > 1:
                result = subprocess.run(CommandWords, capture_output=True, text=True)
        else:
                result = subprocess.run(Command, capture_output=True, text=True)
        print (result.stdout)
        return ( result )
