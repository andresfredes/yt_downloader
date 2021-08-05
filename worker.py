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

"""worker.py: A simple worker function to allow the gui to perform slow
downloads without locking the interface.
"""

from PyQt5.QtCore import QObject, pyqtSignal
from youtube import Downloader

class Worker(QObject):
    """Simple worker class to manage the downloads on a different thread.

    Thread management is done by the GUI itself, but this is the object that
    will get passed to the secondary thread to manage the slow tasks. This uses
    a Downloader object from youtube.py

    Class variables:
        finished (pyqtSignal): Signal emitted to main thread when task complete.
        warning (pyqtSignal): Signal emitted to main thread when task failed.

    Args:
        urls (list): collection of strings representing the video URLs.
        path (str): the path to download videos to.
    """
    finished = pyqtSignal()
    warning = pyqtSignal(int)

    def __init__(self, urls, path):
        super().__init__()
        self.urls = urls
        self.path = path
        self.dl = Downloader()

    def run(self):
        """Activates the downloading of videos passed in during the worker's
        instantiation.
        """
        for url_holder in self.urls:
            url = url_holder.get_url()
            stream_type = url_holder.get_stream_type()
            index = url_holder.index
            if url != "":
                try:
                    self.dl.download(url, self.path, stream_type, index)
                except Exception as e:
                    self.warning.emit(index)
        self.finished.emit()
