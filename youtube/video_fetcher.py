import requests
import pathlib
import pytube


from PyQt5.QtCore import pyqtSignal, QThread, pyqtSlot
import youtube.constants as constants

class VideoFetcher(QThread):

    video_thumbnail_fetch_signal = pyqtSignal(str)
    video_stream_quality_signal = pyqtSignal([list])
    invalid_video_format = pyqtSignal()

    def __init__(self, video_url):
        super(VideoFetcher, self).__init__()
        self.video_url = video_url
        self.video_id  = self._parse_video_id()
        self.current_path = pathlib.WindowsPath().cwd()

    def _parse_video_id(self):
        video_url = ''
        try:
            video_url = pytube.extract.video_id(self.video_url)
        except Exception as e:
            self.invalid_video_format.emit()
            return video_url
        return video_url


    def _generate_youtube_thumbnail_url(self):
        return (constants.youtube_thumbnail_image_url_prefix
                + self.video_id
                + constants.youtube_thumbnail_image_url_image)


    @pyqtSlot()
    def run(self):
        thumbnail_url = self._generate_youtube_thumbnail_url()
        thumbnail_save_path = (self.current_path.joinpath(constants.youtube_media_path)
                            .joinpath(constants.youtube_thumbnails_path)
                            .joinpath(self.video_id))
        image_path = str(thumbnail_save_path) + constants.youtube_thumbnails_ext

        f = open(image_path,'wb')
        f.write(requests.get(thumbnail_url).content)
        f.close()
        try:
            youtube_video = pytube.YouTube(self.video_url)
        except Exception as e:
            self.invalid_video_format.emit()
            return
        youtube_video_streams = youtube_video.streams.filter(adaptive=True).all()
        stream_quality = set([])
        for quality in youtube_video_streams:
            if quality.mime_type == constants.video_mime_type:
                stream_quality.add((quality.itag, quality.resolution))
        self.video_thumbnail_fetch_signal.emit(image_path)
        self.video_stream_quality_signal.emit(list(stream_quality))
