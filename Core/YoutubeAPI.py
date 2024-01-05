from youtube_upload.client import YoutubeUploader

class YoutubeAPI:
    _instance = None

    def __init__(self):
        self.uploader = None

    @staticmethod
    def GetInstance():
        if YoutubeAPI._instance is None:
            YoutubeAPI._instance = YoutubeAPI()
        return YoutubeAPI._instance

    def Initialize(self):
        self.uploader = YoutubeUploader()
        self.uploader.authenticate()

    def DisConnectAPI(self):
        if self.uploader:
            self.uploader.close()

    def UploadVideo(self, filepath):
        if not self.uploader:
            self.Initialize()
        self.uploader.upload(filepath)