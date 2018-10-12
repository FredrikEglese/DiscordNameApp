import asyncio
from discord.ext.commands import Bot
import csv

import os

client = Bot(command_prefix=".")

namesFileName = "names.txt"
helpFileName = "help.txt"

@client.command()
async def add(*args):
	if (len(args) < 2):
		await client.say("Invalid number of arguments.")
	else:
		arguments = args
		user = args[0]
		args = args[1:]
		real_name = ' '.join(args)
		writeToFile(namesFileName,user, real_name)

@client.command()
async def test(*args):
	await client.say(args[0])

@client.command()
async def whois(*args):
	""" Function avaliable to access from users. """
	if(len(args)!=1):
		print("Too many arguments.")
	else:
		returnedName = returnName(namesFileName, args[0])
		if returnedName == 0:
			await client.say("I don't know who "+args[0]+" is.")
		else:
			await client.say(args[0]+" is "+returnedName)

@client.command()
async def printFile(fileName):
	""" Prints out the test from the helpfile. """
	file = open(fileName,'r')
	for line in file:
		await client.say(line)

@client.command()
async def ping():
	await client.say("Pong.")

@client.command()
async def victory():
	await client.say("!play https://www.youtube.com/watch?v=skVg5FlVKS0")

@client.command()
async def loss():
	await client.say("!play https://www.youtube.com/watch?v=9RAbYECBpVA")

@client.event
async def on_ready():
	""" Checks that the necesary files are avaliable. """
	checkForFile(namesFileName)
	checkForFile(helpFileName)
	print("Start up complete.")


def checkForFile(fileName):
	""" If the file already excists, then it is opened then closed.
		If it did not excist already, it will be created.
	"""
	if (os.path.isfile(fileName)==False):
		file = open(fileName,'w')
		file.close()

def readFileContence(fileName):
	""" Returns a dictionary of names in the format {userName: realName}. """
	file = open(namesFileName,'r')
	outputDictionary = {}
	with file as csvfile:
		reader = csv.reader(csvfile, delimiter=',', quotechar='|')
		for line in reader:
			if(len(line) == 2):
				outputDictionary[line[0]] = line[1]
	file.close()
	return(outputDictionary)

def returnName(fileName, userName):
	""" Returns the real name asociated with the provided user name.
		Returns 0 if there is no record of this user name.
	"""
	nameDictionary = readFileContence(fileName)
	if userName in nameDictionary:
		return(nameDictionary[userName])
	else:
		return(0)

def writeToFile(fileName,userName, realName):
	""" Adds the userName realName combination to the names file."""
	file = open(fileName,'a')
	with file as csvfile:
		writter = csv.writer(csvfile, delimiter=',',quotechar='|',
										quoting = csv.QUOTE_MINIMAL)
		writter.writerow([userName, realName])
	file.close()
	

client.run()
