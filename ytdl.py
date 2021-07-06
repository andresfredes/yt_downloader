from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton

from config import *
import sys

class YTDL_Window(QMainWindow):
    def __init__(self):
        super(YTDL_Window, self).__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(WIN["X"], WIN["Y"], WIN["WIDTH"], WIN["HEIGHT"])
        self.setWindowTitle("YouTube downloader")

        self.urlLabel = QLabel(self)
        self.urlLabel.move(URL_LABEL["X"], URL_LABEL["Y"])
        self.urlLabel.setText("Enter YouTube URLs below:")
        self.urlLabel.adjustSize()

        self.dl_button = QPushButton(self)
        self.dl_button.move(DL_BUTTON["X"], DL_BUTTON["Y"])
        self.dl_button.setText("Download")
        self.dl_button.clicked.connect(self.download)

    def download():
        pass

def window():
    app = QApplication(sys.argv)
    win = YTDL_Window()
    win.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    window()
