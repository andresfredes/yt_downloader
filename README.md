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

Requirements:
-------------
Python 3.8+
PyQt5
Packages listed in requirements.txt

License:
--------
Copyright 2021, Andres Fredes, <andres.hector.fredes@gmail.com>

This file is part of yt_downloader.

yt_downloader is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

yt_downloader is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with yt_downloader.  If not, see <https://www.gnu.org/licenses/>.