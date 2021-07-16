from PyQt5.QtCore import QObject, QThread, pyqtSignal

from youtube import Downloader

class Worker(QObject):
    finished = pyqtSignal()
    warning = pyqtSignal(int)

    def __init__(self, urls, path):
        super().__init__()
        self.urls = urls
        self.path = path
        self.dl = Downloader()

    def run(self):
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
