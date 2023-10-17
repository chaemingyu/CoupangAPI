import pixabay.core
from PIL import Image
from Common.CommonAPI import CommonAPI

class PixabayAPI(CommonAPI):

    px = None
    API_KEY = None
    ImageList = []
    def __init__(self):
        self.Initialize()
        # pass

    @staticmethod
    def GetInstance():
        if PixabayAPI._instance is None:  # 인스턴스가 아직 없으면 생성
            PixabayAPI._instance = PixabayAPI()
        return PixabayAPI._instance

    def Initialize(self):
        API_KEY = '40053999-2b85d1718a7ec3f2d658c6ade'
        self.ConnectAPI()
        pass

    def ConnectAPI(self):
        self.px = pixabay.core(self.API_KEY)
        pass

    def DownLoadImages(self, keyword, count):
        self.ImageList = self.px.query(keyword)
        # 첫 번째 인덱스의 이미지를 다운로드 함.
        # 몇 개 검색했는지 나옴
        print("{} hits".format(len(self.ImageList)))
        # 첫 번째 인덱스의 이미지를 다운로드 함.
        self.ImageList[count].download(keyword + str(count) + ".jpg", "largeImage")
        pass