from youtube_upload.client import YoutubeUploader
from Utils import  CommonUtils, CSVManager
import os
from datetime import datetime

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

    def ReadScript(self, file_path):
        # CSV 파일에서 데이터 읽기
        # read_data = CommonUtils.read_from_csv(os.path.join(output_directory, 'data.csv'))
        # print(read_data)  # 읽어온 데이터 출력
        pass

    def CreateScript(self, file_path ,description = None):
        output_directory = os.path.dirname(file_path)
        file_name = os.path.basename(file_path)  # 파일 이름 가져오기
        file_name_without_extension = os.path.splitext(file_name)[0]  # 확장자를 제외한 파일 이름 추출

        data = {
            "title": f"{file_name_without_extension} Top10!! 요즘 인기있는 {file_name_without_extension} 구매 가격 평점 후기 비교 총정리!!",
            "description": self.ReadDescription(description),
            "tags": ["쿠팡", "테스트", "완료"],
            "categoryId": "22",
            "privacyStatus": "public",
            "kids": False,
            "thumbnailLink": "https://cdn.havecamerawilltravel.com/photographer/files/2020/01/youtube-logo-new-1068x510.jpg"
        }

        CommonUtils.save_to_csv(data, os.path.join(output_directory, 'script.csv'))

    def CreateDescription(self, file_path):
        output_directory = os.path.dirname(file_path)

        file_name = os.path.basename(file_path)  # 파일 이름 가져오기
        file_name_without_extension = os.path.splitext(file_name)[0]  # 확장자를 제외한 파일 이름 추출

        script_template = f"❤️❤️❤️ 요즘 인기있는 {file_name_without_extension} 구매 가격 평점 후기 비교 총정리해 보았어요!!\n\n"

        if file_path:
            csv_data = CSVManager.ReadCsvFile(file_path)

            for index, row in csv_data.iterrows():
                time = str(datetime.now().strftime("%Y%m%d")) + "기준"  # 현재 년월일을 YYYYMMDD 형식으로 가져오기
                rank = row['1']
                hashtag = '#' + row['6']
                product = row['3']
                price = str(row['4']) + '원'
                link = row['9'][2:-2]

                script_template += f"❤️❤️❤️ [{time}] {rank}위. {hashtag} {product} [{price}] 💙구매링크👉{link}\n"

            script_template += "❤️상품품절시 구매링크👉https://link.coupang.com/a/5PTJb #샤오미로봇청소기추천 #샤오미로봇청소기가격 #샤오미로봇청소기후기 #샤오미로봇청소기순위 #가성비샤오미로봇청소기 #최저가샤오미로봇청소기 이 포스팅은 쿠팡파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다."

            # 최종 파일 경로
            output_file_path = os.path.join(output_directory, "description.txt")
            CommonUtils.SaveTextFile(script_template,output_file_path)

            return output_file_path

    def ReadDescription(self, file_path):
        return CommonUtils.ReadTextFile(file_path)