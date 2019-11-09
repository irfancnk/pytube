from PyQt5.QtCore import pyqtSignal, QThread, pyqtSlot
import requests
import pathlib
import pytube
import youtube.constants as constants


class VideoDownloader(QThread):

    video_downloaded = pyqtSignal()

    def __init__(self, quality, video_url, stream_qualities):
        super(VideoDownloader, self).__init__()
        self.video_url = video_url
        self.video_quality = quality
        self.stream_qualities = stream_qualities
        self.current_path = pathlib.WindowsPath().cwd()


    def find_quality_itag(self, quality):
        for quality in self.stream_qualities:
            if quality[1] == self.video_quality:
                return str(quality[0])


    @pyqtSlot()
    def run(self):
        video_instance = pytube.YouTube(self.video_url)
        video_save_path = (self.current_path.joinpath(constants.youtube_media_path)
                           .joinpath(constants.youtube_output_path))
        video_stream = video_instance.streams.get_by_itag(self.find_quality_itag(self.video_quality))
        print("Downloading Video")
        video_stream.download(video_save_path)
        print("Download Complete")
