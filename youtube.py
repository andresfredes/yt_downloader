# Copyright 2021, Andres Fredes, <andres.hector.fredes@gmail.com>

# This file is part of yt_downloader.
 
#     yt_downloader is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.

#     yt_downloader is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.

#     You should have received a copy of the GNU General Public License
#     along with yt_downloader.  If not, see <https://www.gnu.org/licenses/>.

"""youtube.py: The core downloading logic and main run file when using the
Command-Line Interface only.

Uses pytube to handle all connection to YouTube.
"""

from pytube import YouTube
from pytube.helpers import safe_filename

class Downloader(object):
    """Handles the downloading from youtube and saving to local filesystem.
    """
    def __init__(self):
        super().__init__()

    def download(self, url, path, stream_type, index=0):
        """Downloads the video at the specified YouTube URL to the specified
        location.

        download can differentiate between audio, video or v+a by using the
        stream_type parameter.

        Args:
            url (str): URL to YouTube video page.
            path (str): Path to save the resultant video file.
                Note: this is passed through a function to ensure the resultant
                filename is safe.
            stream_type (str): "Audio", "Video" or "V+A"
            index (int, optional): Filename prefix for ordering. Defaults to 0.
        """
        yt = YouTube(url)
        prefix = str(index) + "_"
        suffix = ".mp4"
        safe_title = f"{prefix}{safe_filename(yt.title, max_length=30)}{suffix}"
        stream = yt.streams
        if stream_type == "Audio":
            stream = stream.filter(only_audio=True).first()
        elif stream_type == "Video":
            stream = yt.streams.filter(only_video=True).first()
        else:
            stream = yt.streams.get_highest_resolution()
        stream.download(path, safe_title)

    def cli_run(self):
        """Runs the Command-Line Interface version of YouTube Downloader.

        Provides text prompts to enter URL and download path. This CLI version
        will always download the video and audio streams.
        """
        url = input("Enter Youtube URL: ")
        path = input("Enter download path: ")
        try:
            self.download(url, path, "V+A")
        except Exception as e:
            print(e)
            print("Video is not available for download")
        else:
            print("Download successful")

if __name__ == '__main__':
    ytdl = Downloader()
    ytdl.cli_run()
