# music-dl
A small program for getting an album from a youtube playlist and tagging it.

## What works
* Downloading albums from youtube
* Converting them to a single format
* Adding artist, album name, and song title to all the songs

## What doesn't (help wanted)
* Adding cover art to songs, currently pushing for ogg support.
* Adding more support for other formats

## How can I get cover support for [music player of choice here]
The majority of _good_ music players (foobar2000, vlc, etc) are satisfied with a simple cover.jpg (or png) in the same directory as the album. So after downloading the album with music-dl, it might be a good idea to grab the cover image and stick it in there so your music player can have the art loaded.

## Requirements
Music-dl uses the following programs to run
* Python 3.6+: Get it from your package manager or from [Python's site](https://python.org)
* youtube-dl: Using pip is the preferred way of getting it, can also be obtained from python's website and installed with `pip3 install youtube-dl`
* ffmpeg: Can be obtained via package manager or from [here](https://ffmpeg.org/)

## Installing
* Obtain a copy of the repository, this can be done by running `git clone https://github.com/taizweb/music-dl.git` or by downloading the zip [here](https://github.com/TaizWeb/music-dl/archive/master.zip)
* Open the src folder and run `python3 music-dl.py` to run the program

## Coming Soon
A front-end 
