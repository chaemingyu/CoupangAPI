from youtube_upload.client import YoutubeUploader
from Utils import  CommonUtils, CSVManager
import os
import csv
from datetime import datetime
import ast
import tkinter as tk
from tkinter import filedialog
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
        data = self.ReadScript(filepath)
        self.uploader.upload(filepath,data)

    # def to_dict(self):
    #     return {
    #             "title": "공개 이미지",
    #             "description": "테스트 설명",
    #             "tags": ["쿠팡", "테스트", "완료"],
    #             "categoryId": "22",
    #             "privacyStatus": "public",
    #             "kids": False,
    #             "thumbnailLink": "https://cdn.havecamerawilltravel.com/photographer/files/2020/01/youtube-logo-new-1068x510.jpg"
    #         }

    def ReadScript(self, filepath):
        folder_path, filename = os.path.split(filepath)
        if folder_path:
            script_path = os.path.join(folder_path, 'script.csv')

            data_dict = {}  # CSV 파일에서 읽은 데이터를 저장할 딕셔너리

            with open(script_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for index, row in enumerate(reader):
                    # 읽은 각 행의 데이터를 to_dict 형식에 맞게 변환하여 딕셔너리에 추가
                    data_dict[index] = {
                        "title": row["title"],
                        "description": row["description"],
                        "tags": ast.literal_eval(row["tags"]),  # 문자열 리스트를 파이썬 리스트로 변환
                        "categoryId": row["categoryId"],
                        "privacyStatus": row["privacyStatus"],
                        "kids": row["kids"] == "True",
                        "thumbnailLink": row["thumbnailLink"]
                    }

        return data_dict

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