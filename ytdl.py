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

"""ytdl.py: Main launcher for the gui version of YouTube Downloader
"""

from PyQt5.QtWidgets import QApplication

from gui import YTDL_Window

import sys

def window():
    app = QApplication(sys.argv)
    win = YTDL_Window()
    win.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    window()
