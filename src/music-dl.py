import subprocess
import os

# TODO: Make ffmpeg be silent and make ffmpeg not reconvert songs
# TODO: User friendlyness
# TODO: Color output

running = True

print("Welcome to music-dl, a tool built on youtube-dl!")

# printOptions: Prints the current options for music-dl
def printOptions():
	print("(d)ownload a new album")
	print("(i)nfo")
	print("(q)uit music-dl")

# downloadPrompt: Prompts the user for a link to the youtube-playlist
def downloadPrompt():
	playlist = input("Enter the playlist URL: ")
	location = input("Enter a folder name for the playlist: ")
	print("Downloading...")
	subprocess.run(["youtube-dl", "-x", playlist], cwd=os.getcwd() + "/" + location)
	print("Album downloaded.")
	convertAlbum(location)

# convertAlbum: Converts the album to the format entered by the user
def convertAlbum(location):
	print("Downloaded albums tend to have songs in multiple filetypes.")
	print("Would you like to convert them?")
	print("Common formats are: ogg, opus, mp3, wav, flac")
	print("ogg is reccomended because it supports metadata and album covers")
	albumFormat = input("Enter a format (no period): ")
	# subprocess.run(["../converter.sh", albumFormat], cwd=os.getcwd() + "/" + location)
	os.chdir(location)
	songs = os.listdir()
	print("Converting album...")
	for song in songs:
		# Exclude images
		if (song[-3:] != "png" and song[-3:] != "jpg" and song[-4:] != "jpeg"):
			songData = song.split(".")
			subprocess.run(["ffmpeg", "-loglevel", "panic", "-i", song, songData[0] + "." + albumFormat])
			print("Removing " + song)
			subprocess.run(["rm", song])

	addMetadata(location)

# addMetadata: Adds the album name, artist, and title to songs
def addMetadata(location):
	songs = os.listdir()
	albumArtist = input("Enter the artist of the album: ")
	albumName = input("Enter the name of the album: ")
	print("Adding metadata...")
	for song in songs:
		print("File:", song)
		songTitle = input("Enter a title: ")
		if (song[-3:] != "png" and song[-3:] != "jpg" and song[-4:] != "jpeg"):
			print("Converting: " + song)
			subprocess.run(["ffmpeg", "-loglevel", "panic", "-i", song, "-metadata", 'album="' + albumName + '"', "-metadata", 'artist="' + albumArtist + '"', "-metadata", 'title="' + songTitle + '"', "new-" + song])
			subprocess.run(["rm", song])
			subprocess.run(["mv", "new-" + song, song])
	addCoverArt(location)

# addCoverArt: Adds coverart to the songs
def addCoverArt(location):
	songs = os.listdir()
	artLocation = input("Enter the filename within '" + location + "' of the cover art (default: cover.png): ")
	if (artLocation == ""):
		artLocation = "cover.png"
	print("Adding cover art...")
	for song in songs:
		print("Adding art to " + song)
		if (song[-3:] != "png" and song[-3:] != "jpg" and song[-4:] != "jpeg"):
			subprocess.run(["ffmpeg", "-loglevel", "panic", "-i", song, "-i", artLocation, "-map_metadata", "0", "-map", "0", "-map", "1", "new-" + song])
			subprocess.run(["rm", song])
			subprocess.run(["mv", "new-" + song, song])

# printInfo: Prints the required dependencies of music-dl
def printInfo():
	print("\nIn order to run music-dl, you need the following installed at their LATEST version:")
	print("Python 3.6+, can be installed from your systems package manager or from python.org, run python -v to check your installed version")
	print("youtube-dl: Installed with 'pip install youtube-dl', can be upgraded with 'pip install --upgrade youtube-dl'")
	print("ffmpeg: Installed/upgraded with your system's package manager. Debian users can run 'sudo apt install ffmpeg'\n")

# The main loop, asks the user for what option to run
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
