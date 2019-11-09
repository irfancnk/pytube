#! /usr/bin/env python

'''
********************************************************************************
This is the entry point of the Network Analyzer Program that uses monitor
classes and  interface.
********************************************************************************
'''

import sys
import qdarkstyle
from PyQt5 import QtWidgets

from interface.youtube_downloader_controller import YoutubeDownloaderController



def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    main_ui = YoutubeDownloaderController()
    ret = app.exec_()
    sys.exit(ret)


if __name__ == '__main__':
    main()




# END
