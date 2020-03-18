import subprocess
import os

running = True

print("Welcome to music-dl, a tool built on youtube-dl!")

def printOptions():
	print("(d)ownload a new album")
	print("(i)nfo")
	print("(q)uit music-dl")

def downloadPrompt():
	playlist = input("Enter the playlist URL: ")
	location = input("Enter a folder name for the playlist: ")
	print("Downloading...")
	subprocess.run(["youtube-dl", "-x", playlist], cwd=os.getcwd() + "/" + location)
	print("Album downloaded.")
	convertAlbum(location)

def convertAlbum(location):
	print("Downloaded albums tend to have songs in multiple filetypes.")
	print("Would you like to convert them?")
	print("Common formats are: ogg, opus, mp3, wav, flac")
	print("ogg is reccomended because it supports metadata and album covers")
	albumFormat = input("Enter a format (no period): ")
	subprocess.run(["./converter.sh", albumFormat], cwd=os.getcwd() + "/" + location)
	cleanupAlbum(location)
	addMetadata(location)

def cleanupAlbum(location):
	pass

def addMetadata(location):
	os.chdir(location)
	songs = os.listdir()
	albumArtist = input("Enter the artist of the album: ")
	albumName = input("Enter the name of the album: ")
	print(songs)
	for song in songs:
		print("Converting: " + song)
		songTitle = input("Enter a title: ")
		subprocess.run(["ffmpeg", "-i", song, "-metadata", 'album="' + albumName + '"', "-metadata", 'artist="' + albumArtist + '"', "-metadata", 'title="' + songTitle + '"', "new-" + song])

def printInfo():
	print("\nIn order to run music-dl, you need the following installed at their LATEST version:")
	print("Python 3.6+, can be installed from your systems package manager or from python.org, run python -v to check your installed version")
	print("youtube-dl: Installed with 'pip install youtube-dl', can be upgraded with 'pip install --upgrade youtube-dl'")
	print("ffmpeg: Installed/upgraded with your system's package manager. Debian users can run 'sudo apt install ffmpeg'")

while (running):
	printOptions()
	selection = input("What would you like to do: ")
	if (selection == "d"):
		downloadPrompt()
	elif (selection == "i"):
		printInfo()
	elif (selection == "q"):
		running = False
	else:
		print("\nInvalid option '" + selection + "'. Usage:")

print("Exiting...")

