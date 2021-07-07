from pytube import YouTube
from pytube.helpers import safe_filename

class Downloader(object):
    def __init__(self):
        super().__init__()

    def download(self, url, path, index=0):
        yt = YouTube(url)
        prefix = str(index) + "_"
        safe_title = prefix + safe_filename(yt.title, max_length=30)
        yt.streams.get_highest_resolution().download(path, safe_title)

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
