import pixabay.core
from Core.CommonAPI import CommonAPI
from youtube_upload.client import YoutubeUploader

class YoutubeAPI(CommonAPI):

    uploader = None

    @staticmethod
    def GetInstance():
        if YoutubeAPI._instance is None:  # 인스턴스가 아직 없으면 생성
            YoutubeAPI._instance = YoutubeAPI()
        return YoutubeAPI._instance
        pass

    @staticmethod
    def Initialize(self):
        uploader = YoutubeUploader()
        uploader.authenticate()

    @staticmethod
    def ConnectAPI(self):
        self.Initialize()

    def DisConnectAPI(self):
        self.uploader.close()

    def Upload(self, filepath):
        filepath = r'C:\Users\godzx\Desktop\JupyterNotbook\output_video.avi'
        self.ploader.upload(filepath)