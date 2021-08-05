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

"""gui.py: The Graphical User Interface for YouTube Downloader.

Uses Qt for creation of the GUI elements as well as handling the secondary
thread required when downloading videos to avoid locking the UI.
"""

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QMainWindow, QLabel, QPushButton, QMessageBox,
    QLineEdit, QHBoxLayout, QVBoxLayout, QWidget, QFileDialog, QRadioButton,
    QButtonGroup)
from PyQt5.QtCore import QThread, Qt

from worker import Worker
from config import *

class YTDL_Window(QMainWindow):
    """Main window for the YouTube Downloader program.

    Holds the Central Widget, which in turns hosts the rest of the widgets.
    """
    def __init__(self):
        super(YTDL_Window, self).__init__()
        self._initUI()

    def _initUI(self):
        ui = Central_Widget()
        self.setCentralWidget(ui)
        self.setGeometry(WIN["X"], WIN["Y"], WIN["WIDTH"], WIN["HEIGHT"])
        self.setWindowTitle("YouTube downloader")

class Central_Widget(QWidget):
    """The host to the widgets that create bulk of the UI.

    Hosts a set of text boxes allowing for URL entry, radio buttons to select
    between stream types and a couple of buttons to allow the user to choose a
    download location and to ultimately start the download.
    """
    def __init__(self):
        super().__init__()
        self.path = ""
        self.urls = []
        self._initUI()

    def _initUI(self):
        rows = QVBoxLayout()

        url_label = QLabel()
        url_label.setText("Enter one or more YouTube URLs below:")
        url_label.adjustSize()
        rows.addWidget(url_label)

        for index in range(1, 1 + MAX_URLS):
            layout = URL_Layout(index)
            self.urls.append(layout)
            rows.addLayout(layout)

        self.info_label = QLabel()
        self.info_label.setText("")
        self.info_label.adjustSize()
        self.info_label.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setPointSize(18)
        self.info_label.setFont(font)
        rows.addWidget(self.info_label)

        rows.addStretch()

        contact_label = QLabel()
        contact_label.setText(
            "Send feedback to: andres.hector.fredes@gmail.com"
        )
        contact_label.adjustSize()
        contact_label.setAlignment(Qt.AlignCenter)
        rows.addWidget(contact_label)

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
        rows.addLayout(buttons)

        self.setLayout(rows)

    def get_path(self):
        """Activated by the path button, to allow a user to choose the download
        location.

        Also triggers the activation of the usually disabled "download" button,
        when a suitable path has been selected.
        """
        dir_picker = QFileDialog()
        self.path = dir_picker.getExistingDirectory(None, "Choose a folder: ")
        if self.path != "":
            self.dl_button.setEnabled(True)

    def download(self):
        """Starts the downloads themselves.

        The host button to this function is disabled by default and will only
        become available for use when the user has chosen a download location.
        To avoid accidental double-clicks, the download button is also disabled
        during downloads and a simple "Downloading..." message is presented.

        Download processing is pushed to a secondary thread to avoid locking the
        UI.
        """
        self.dl_button.setEnabled(False)
        self.info_label.setText("Downloading...")

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
            lambda: self.info_label.setText("Download complete!")
        )

    def warning(self, index):
        """Generates a pop-up warning that a download failed.

        Triggered by an incoming signal from the secondary thread.

        Args:
            index (int): The index of the video that failed.
        """
        title = "Download error"
        message = "Video #" + str(index) + " unavailable"
        warning = QMessageBox.warning(
            None, title, message, QMessageBox.Ok, QMessageBox.Ok)

class URL_Layout(QHBoxLayout):
    """A layout composed of a URL textbox, label and radio button group.

    This allows for all of the controls associated with each video download to 
    be inserted into the UI together, and therefore many URLs can be collected
    without much additional code.

    Args:
        index (int): Number for id'ing elements and naming output files.
    """
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
