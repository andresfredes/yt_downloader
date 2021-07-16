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
