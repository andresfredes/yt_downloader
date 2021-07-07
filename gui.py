from PyQt5.QtWidgets import (QMainWindow, QLabel, QPushButton, QMessageBox,
    QLineEdit, QHBoxLayout, QVBoxLayout, QWidget, QFileDialog)

from youtube import *
from config import *

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
        self.path = ""
        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout(self)

        url_Label = QLabel(self)
        url_Label.setText("Enter YouTube URLs below:")
        url_Label.adjustSize()
        vbox.addWidget(url_Label)

        textbox = QLineEdit(self)
        vbox.addWidget(textbox)

        path_button = QPushButton(self)
        path_button.setText("Choose download location")
        path_button.clicked.connect(self.get_path)
        vbox.addWidget(path_button)

        dl_button = QPushButton(self)
        dl_button.setText("Download")
        dl_button.clicked.connect(self.download)
        vbox.addWidget(dl_button)

        self.setLayout(vbox)

    def get_path(self):
        dir_picker = QFileDialog()
        self.path = dir_picker.getExistingDirectory(None, "Choose a folder: ")

    def download(self):
        if self.path == "":
            self.no_path_warning()

    def no_path_warning(self):
        choose_button = Choose_Button(self)

        warning = QMessageBox.warning(
            None,
            "Download location not selected",
            "Download location not selected",
            choose_button | QMessageBox.Ok,
            choose_button
        )

class Choose_Button(QPushButton):
    def __init__(self, widget):
        super.__init__()
        self.setText("Choose")
        self.clicked.connect(widget.get_path)
