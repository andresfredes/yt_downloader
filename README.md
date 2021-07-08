YouTube Downloader
==================

Description:
------------
A simple CLI or GUI program that takes YouTube URLs as input and downloads the
corresponding video at the highest resolution available.

Usage:
------
### Command line:
`python youtube.py`
This will prompt for the URL and download path.

### Graphical User Interface:
`python ytdl.py`
The GUI will be generated, allowing for batching of up to 9 URLs at a time.

### Executables:
Pyinstaller has been listed in requirements.txt to allow for easy packaging.
`pyinstaller -wF ytdl.py` Generates a local OS specific executable with all
dependancies included in a single file.

Files:
------
## config.py
Some basic configuration variables, primarily GUI window sizing

## gui.py
The GUI classes using PyQt5

## README.md
This file

## requirements.txt
All packages required for the program to run. Also includes PyInstaller, to
allow for packaging into executable.

## worker.py
A worker class to allow for thread work in the GUI, to avoid locking.

## youtube.py
YouTube downloader logic and CLI code.

## ytdl.py
GUI main file
