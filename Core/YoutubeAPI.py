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

        self.uploader.upload(filepath,self.to_dict())

    def to_dict(self):
        return {
                "title": "공개 이미지",
                "description": "테스트 설명",
                "tags": ["쿠팡", "테스트", "완료"],
                "categoryId": "22",
                "privacyStatus": "public",
                "kids": False,
                "thumbnailLink": "https://cdn.havecamerawilltravel.com/photographer/files/2020/01/youtube-logo-new-1068x510.jpg"
            }