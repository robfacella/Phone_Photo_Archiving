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
def TimeDilation(Command):
        CommandWords = Command.split(" ")
        newWords = [CommandWords[0], CommandWords[1], f"\"{CommandWords[2]} {CommandWords[3]}\""]
        CommandWords = newWords
        print (f"{CommandWords}")
        if len(CommandWords) > 1:
                result = subprocess.run(CommandWords, capture_output=True, text=True)
        else:
                result = subprocess.run(Command, capture_output=True, text=True)
        print (result.stdout)
        return ( result )
