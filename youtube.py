from pytube import YouTube
from pytube.helpers import safe_filename

def download(yt, path, index=0):
    safe_title = safe_filename(yt.title, max_length=30)
    prefix = str(index) + "_"
    yt.streams.get_highest_resolution().download(path, safe_title)

def get_youtube(url):
    return YouTube(url)

def get_filesize(yt):
    size_bytes = yt.filesize_approx()

def cli_run():
    url = input("Enter Youtube URL: ")
    path = input("Enter download path: ")
    try:
        yt = get_youtube(url)
    except VideoUnavailable:
        print("Video is not available for download")
    else:
        download(yt, path)
        print("Download successful")

if __name__ == '__main__':
    cli_run()
