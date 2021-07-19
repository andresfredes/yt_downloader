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

from pytube import YouTube
from pytube.helpers import safe_filename

class Downloader(object):
    def __init__(self):
        super().__init__()

    def download(self, url, path, stream_type, index=0):
        yt = YouTube(url)
        prefix = str(index) + "_"
        safe_title = prefix + safe_filename(yt.title, max_length=30)
        stream = yt.streams
        if stream_type == "Audio":
            stream = stream.filter(only_audio=True).first()
        elif stream_type == "Video":
            stream = yt.streams.filter(only_video=True).first()
        else:
            stream = yt.streams.get_highest_resolution()
        stream.download(path, safe_title)

    def cli_run(self):
        url = input("Enter Youtube URL: ")
        path = input("Enter download path: ")
        try:
            self.download(url, path)
        except Exception as e:
            print(e)
            print("Video is not available for download")
        else:
            print("Download successful")

if __name__ == '__main__':
    ytdl = Downloader()
    ytdl.cli_run()
