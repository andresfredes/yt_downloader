from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QPushButton,
    QLineEdit, QHBoxLayout, QVBoxLayout, QWidget)

from config import *
import sys

class YTDL_Window(QMainWindow):
    def __init__(self):
        super(YTDL_Window, self).__init__()
        self.initUI()

    def initUI(self):
        ui = Central_Widget()
        self.setCentralWidget(ui)
        self.setGeometry(WIN["X"], WIN["Y"], WIN["WIDTH"], WIN["HEIGHT"])
        self.setWindowTitle("YouTube downloader")

class Central_Widget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout(self)

        url_Label = QLabel(self)
        url_Label.setText("Enter YouTube URLs below:")
        url_Label.adjustSize()
        vbox.addWidget(url_Label)

        textbox = QLineEdit(self)
        vbox.addWidget(textbox)

        dl_button = QPushButton(self)
        dl_button.setText("Download")
        dl_button.clicked.connect(self.download)
        vbox.addWidget(dl_button)

        self.setLayout(vbox)

    def download(self):
        pass

def window():
    app = QApplication(sys.argv)
    win = YTDL_Window()
    win.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    window()
