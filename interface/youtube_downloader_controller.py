# START

import pathlib
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from interface.youtube_downloader_generator import Ui_MainWindow
from youtube.video_downloader import VideoDownloader
from youtube.video_fetcher import VideoFetcher


class YoutubeDownloaderController(Ui_MainWindow):

    def __init__(self):
        Ui_MainWindow.__init__(self)
        self.MainWindow = QtWidgets.QMainWindow()
        self.video_fetcher = None
        self.video_downloader = None
        self.all_video_qualities = None
        self.initialize_gui()



    def initialize_gui(self):
        self.setupUi(self.MainWindow)
        self.MainWindow.show()
        self.connect_callbacks()

    def connect_callbacks(self):
        self.pushButton_fetch.clicked.connect(self.fetch_video)
        self.pushButton.clicked.connect(self.download_video)

    def fetch_video(self):
        video_url = self.lineEdit_url.text()
        self.lineEdit_url.clear()
        self.lineEdit_url.setPlaceholderText('Please wait...')
        self.lineEdit_url.setEnabled(False)
        self.video_fetcher = VideoFetcher(video_url)
        self.video_fetcher.video_thumbnail_fetch_signal.connect(self.brush_thumbnail)
        self.video_fetcher.video_stream_quality_signal.connect(self.generate_dropdown)
        self.video_fetcher.invalid_video_format.connect(self.invalid_url_entered)
        self.video_fetcher.start()

    def invalid_url_entered(self):
        self.lineEdit_url.setEnabled(True)
        self.lineEdit_url.setPlaceholderText('Entered URL was invalid.')
        self.pushButton.setEnabled(False)
        self.comboBox_quality.setEnabled(False)


    def brush_thumbnail(self, image_path):

        self.video_fetcher.video_thumbnail_fetch_signal.disconnect()
        qpixmap = QPixmap(image_path)
        resized_pixmap = qpixmap.scaled(550, 200, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.qlabel_thumbnail.setPixmap(resized_pixmap)


    def generate_dropdown(self, all_stream_qualities):
        self.all_video_qualities = all_stream_qualities
        stream_qualities = []
        self.lineEdit_url.setPlaceholderText('https://www.youtube.com/watch?v=G1IbRujko-A')
        self.lineEdit_url.setEnabled(True)
        for quality in all_stream_qualities:
            if quality[1] is not None:
                stream_qualities.append(quality[1])
        stream_qualities.sort()
        self.comboBox_quality.setEnabled(True)
        self.comboBox_quality.clear()
        self.comboBox_quality.addItems(stream_qualities)
        self.pushButton.setEnabled(True)


    def download_video(self):
        self.video_downloader = VideoDownloader(self.comboBox_quality.currentText(), self.video_fetcher.video_url, self.all_video_qualities)
        self.video_downloader.start()
