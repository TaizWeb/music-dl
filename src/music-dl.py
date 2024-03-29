import subprocess
import os

running = True
formats = ["ogg", "opus", "mp3", "wav", "flac"]

print("Welcome to music-dl, a tool built on youtube-dl!")

# printOptions: Prints the current options for music-dl
def printOptions():
	print("(d)ownload a new album")
	print("(e)dit an existing album")
	print("(i)nfo")
	print("(q)uit music-dl")

# editAlbum: Allows a user to edit an existing album
def editAlbum():
	editorFolder = input("Enter folder name of the album: ")

	while not os.path.isdir(editorFolder):
		print("Folder " + editorFolder + " could not be found.")
		editorFolder = input("Enter folder name of the album: ")

	os.chdir(editorFolder)
	addMetadata(editorFolder)

# verifyFolder: Prompts the user until a new folder is created, or an existing one is entered
def verifyFolder(location):
	if os.path.isdir(location):
		return location
	else:
		print("The folder '" + location + "' doesn't exist.")
		newFolder = input("Create one? (note that it'll need a cover image inside later) [y/n]: ")
		if (newFolder == "y"):
			os.mkdir(location)
			print("Folder '" + location + "' created!")
			return location
		else:
			location = verifyFolder(input("Enter a folder name for the playlist: "))
	return location

# verifyFormat: Checks if the entered file format is supported
def verifyFormat(fileFormat):
	if (fileFormat in formats):
		return fileFormat
	else:
		print("Supported formats: ogg, opus, mp3, wav, flac")
		fileFormat = verifyFormat(input("Enter a format: "))
	return fileFormat

# verifyArt: Checks if the cover art exists
def verifyArt(artLocation):
	if (os.path.isfile(artLocation)):
		return artLocation
	else:
		print("Cover art at '" + artLocation + "' doesn't exist.")
		artLocation = verifyArt(input("Enter the cover art location: "))
	return artLocation

# downloadPrompt: Prompts the user for a link to the youtube-playlist
def downloadPrompt():
	playlist = input("Enter the playlist URL: ")
	location = verifyFolder(input("Enter a folder name for the playlist: "))
	print("Downloading...")
	subprocess.run(["yt-dlp", "-x",  playlist], cwd=os.getcwd() + "/" + location)
	print("Album downloaded.")
	convertAlbum(location)

# convertAlbum: Converts the album to the format entered by the user
def convertAlbum(location):
	print("Downloaded albums tend to have songs in multiple filetypes.")
	print("Would you like to convert them?")
	print("Common formats are: ogg, opus, mp3, wav, flac")
	print("ogg is reccomended because it supports metadata and album covers")
	albumFormat = verifyFormat(input("Enter a format (no period): "))
	os.chdir(location)
	songs = os.listdir()
	print("Converting album...")
	for song in songs:
		# Exclude images
		if (song[-3:] != "png" and song[-3:] != "jpg" and song[-4:] != "jpeg"):
			songData = song.split(".")
			# Append everything prior to the extension
			for i in range(len(songData)):
				if i+1 < len(songData):
					songData[0] += songData[i+1]
			# ffmpeg convert
			subprocess.run(["ffmpeg", "-loglevel", "panic", "-i", song, songData[0] + "." + albumFormat])
			print("Removing " + song)
			subprocess.run(["rm", song])

	addMetadata(location)

# addMetadata: Adds the album name, artist, and title to songs
def addMetadata(location):
	songs = os.listdir()
	albumArtist = input("Enter the artist of the album: ")
	albumName = input("Enter the name of the album: ")

	# Delimiter
	print("Would you like a delimiter? Ex. Setting the delimiter to '-':\nSong Title - Album Name -> Song Title")
	delimiter = input("Enter delimiter (blank for none): ")
	if delimiter:
		songSplit = songs[0].split(delimiter)
		print("For '" + songs[0] + "' this would result in:")
		for index, split in enumerate(songSplit):
			print("[" + str(index+1) + "] " + split)
		delimitIndex = int(input("Which index should be used: "))

	# Add the meta data
	print("Adding metadata...")
	for song in songs:
		if (song[-3:] != "png" and song[-3:] != "jpg" and song[-4:] != "jpeg"):
			print("File:", song)
			if delimiter:
				print("Delimited:", song.split(delimiter)[delimitIndex-1])
			songTitle = input("Enter a title (blank to leave as-is): ")
			if not songTitle:
				if not delimiter:
					songTitle = song
				else:
					songTitle = song.split(delimiter)[delimitIndex-1]

			# Writing metadata
			subprocess.run(["ffmpeg", "-loglevel", "panic", "-i", song, "-map_metadata", "-1", "-metadata", 'album=' + albumName, "-metadata", 'artist=' + albumArtist, "-metadata", 'title=' + songTitle, "-acodec", "copy", "new-" + song])
			subprocess.run(["rm", song])
			subprocess.run(["mv", "new-" + song, song])
	os.chdir("..")
	# addCoverArt(location)

# addCoverArt: Adds coverart to the songs
def addCoverArt(location):
	songs = os.listdir()
	artLocation = verifyArt(input("Enter the filename within '" + location + "' of the cover art (default: cover.png): "))
	if (artLocation == ""):
		artLocation = "cover.png"
	print("Adding cover art...")
	for song in songs:
		if (song[-3:] != "png" and song[-3:] != "jpg" and song[-4:] != "jpeg"):
			print("Adding art to " + song)
			subprocess.run(["ffmpeg", "-loglevel", "panic", "-i", song, "-i", artLocation, "-map_metadata", "0", "-map", "0", "-map", "1", "-acodec", "copy", "new-" + song])
			subprocess.run(["rm", song])
			subprocess.run(["mv", "new-" + song, song])
	os.chdir("..")

# printInfo: Prints the required dependencies of music-dl
def printInfo():
	print("\nIn order to run music-dl, you need the following installed at their LATEST version:")
	print("Python 3.6+: Can be installed from your systems package manager or from python.org, run python -v to check your installed version")
	print("youtube-dl: Installed with 'pip install youtube-dl', can be upgraded with 'pip install --upgrade youtube-dl'")
	print("ffmpeg: Installed/upgraded with your system's package manager. Debian-based users can run 'sudo apt install ffmpeg'\n")

# The main loop, asks the user for what option to run
while (running):
	printOptions()
	selection = input("What would you like to do: ")
	if (selection == "d"):
		downloadPrompt()
	elif (selection == "e"):
		editAlbum()
	elif (selection == "i"):
		printInfo()
	elif (selection == "q"):
		running = False
	else:
		print("\nInvalid option '" + selection + "'. Usage:")

print("Exiting...")

