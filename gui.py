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

from PyQt5.QtWidgets import (QMainWindow, QLabel, QPushButton, QMessageBox,
    QLineEdit, QHBoxLayout, QVBoxLayout, QWidget, QFileDialog, QRadioButton,
    QButtonGroup)
from PyQt5.QtCore import QObject, QThread

from worker import Worker
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
        self.urls = []
        self.initUI()

    def initUI(self):
        rows = QVBoxLayout()

        url_Label = QLabel()
        url_Label.setText("Enter one or more YouTube URLs below:")
        url_Label.adjustSize()
        rows.addWidget(url_Label)

        for index in range(1, 1 + MAX_URLS):
            layout = URL_Layout(index)
            self.urls.append(layout)
            rows.addLayout(layout)

        self.info_Label = QLabel()
        self.info_Label.setText("")
        self.info_Label.adjustSize()
        rows.addWidget(self.info_Label)

        buttons = QHBoxLayout()

        path_button = QPushButton()
        path_button.setText("Choose download location")
        path_button.clicked.connect(self.get_path)
        buttons.addWidget(path_button)

        self.dl_button = QPushButton()
        self.dl_button.setText("Download")
        self.dl_button.setEnabled(False)
        self.dl_button.clicked.connect(self.download)
        buttons.addWidget(self.dl_button)

        rows.addStretch()
        rows.addLayout(buttons)

        self.setLayout(rows)

    def get_path(self):
        dir_picker = QFileDialog()
        self.path = dir_picker.getExistingDirectory(None, "Choose a folder: ")
        if self.path != "":
            self.dl_button.setEnabled(True)

    def download(self):
        self.dl_button.setEnabled(False)
        self.info_Label.setText("Downloading...")

        self.thread = QThread()
        self.worker = Worker(self.urls, self.path)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.warning.connect(self.warning)
        self.thread.start()

        self.thread.finished.connect(
            lambda: self.dl_button.setEnabled(True)
        )
        self.thread.finished.connect(
            lambda: self.info_Label.setText("Download complete!")
        )

    def warning(self, index):
        title = "Download error"
        message = "Video #" + str(index) + " unavailable"
        warning = QMessageBox.warning(
            None, title, message, QMessageBox.Ok, QMessageBox.Ok)

class URL_Layout(QHBoxLayout):
    def __init__(self, index):
        super().__init__()
        self.index = index
        self.stream = "V+A"

        index_label = QLabel()
        index_label.setText(str(self.index))
        self.addWidget(index_label)

        self.textbox = QLineEdit()
        self.addWidget(self.textbox)

        self.r_group = QButtonGroup()
        r1 = Custom_Radio("Audio", self)
        self.r_group.addButton(r1)
        self.addWidget(r1)
        r2 = Custom_Radio("Video", self)
        self.r_group.addButton(r2)
        self.addWidget(r2)
        r3 = Custom_Radio("V+A", self)
        self.r_group.addButton(r3)
        r3.setChecked(True)
        self.addWidget(r3)

    def set_stream(self, text):
        self.stream = text

    def get_stream_type(self):
        return self.stream

    def get_url(self):
        return self.textbox.text()

class Custom_Radio(QRadioButton):
    def __init__(self, text, layout):
        super().__init__()
        self.layout = layout
        self.text = text
        self.setText(self.text)
        self.toggled.connect(self.on_clicked)

    def on_clicked(self):
        radio = self.sender()
        if radio.isChecked():
            self.layout.set_stream(self.text)
