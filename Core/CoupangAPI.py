import cv2
import os
import hmac
import hashlib
import requests
import json
from time import gmtime, strftime
import urllib.request
import numpy as np
from io import BytesIO
from urllib.parse import urlencode
from Core.CommonAPI import CommonAPI
from datetime import datetime
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import pandas as pd
from Utils import  CommonUtils, CSVManager
from Common import  Config
from PIL import Image, ImageDraw, ImageFont
import tkinter as tk
from tkinter import filedialog
from moviepy.editor import VideoFileClip, AudioFileClip

class CoupangAPI(CommonAPI):

    REQUEST_METHOD = None
    DOMAIN = "https://api-gateway.coupang.com"
    URL = None
    REQUEST = None
    # Replace with your own ACCESS_KEY and SECRET_KEY
    ACCESS_KEY = "9a6f6be2-96ff-4a2a-9c50-e16262589987"
    SECRET_KEY = "ac68c2ba170e765c2dd548a2a0dfab6d48a87377"
    _instance = None  # 클래스 레벨에서 정적 변수로 선언
    DRIVER = None
    Category = Config.ShoppingCategory
    file_path = ""
    def __init__(self):
        # self.Initialize()
        pass

    @staticmethod
    def GetInstance():
        if CoupangAPI._instance is None:  # 인스턴스가 아직 없으면 생성
            CoupangAPI._instance = CoupangAPI()
        return CoupangAPI._instance

    def Initialize(self):
        try:
            # self.ConnectAPI()

            # Chrome 옵션 초기화
            chrome_options = Options()
            chrome_options.add_argument("--headless")  # 브라우저를 표시하지 않고 백그라운드에서 실행

            # Chrome 웹 드라이버 초기화 - ChromeDriverManager를 이용하여 자동으로 최신 버전의 chromedriver 다운로드
            driver_path = ChromeDriverManager().install()
            self.DRIVER = webdriver.Chrome(driver_path, options=chrome_options)

        except Exception as e:
            print(f'Initialize 에러 발생: {e}')




        # self.SelectBestCategory("1001")
        # self.WirteImage()
        pass

    # HMAC 서명 생성 및 API 호출
    def generateHmac(self,method, url, secretKey, accessKey):
        path, *query = url.split("?")
        datetimeGMT = strftime('%y%m%d', gmtime()) + 'T' + strftime('%H%M%S', gmtime()) + 'Z'
        message = datetimeGMT + method + path + (query[0] if query else "")

        signature = hmac.new(bytes(secretKey, "utf-8"),
                             message.encode("utf-8"),
                             hashlib.sha256).hexdigest()

        return "CEA algorithm=HmacSHA256, access-key={}, signed-date={}, signature={}".format(accessKey, datetimeGMT, signature)

    def GetAuthorization(self):
        return self.generateHmac(self.REQUEST_METHOD, self.URL, self.SECRET_KEY, self.ACCESS_KEY)


    def ConnectAPI(self):
        #API 호출
        self.REQUEST_METHOD = "POST"
        self.URL = "/v2/providers/affiliate_open_api/apis/openapi/v1/deeplink"

        self.REQUEST = {"coupangUrls": [
            "https://www.coupang.com/np/search?component=&q=good&channel=user",
            "https://www.coupang.com/np/coupangglobal"
        ]}

        authorization = self.GetAuthorization()
        url = "{}{}".format(self.DOMAIN, self.URL)
        response = requests.request(method=self.REQUEST_METHOD, url=url,
                                    headers={
                                        "Authorization": authorization,
                                        "Content-Type": "application/json"
                                    },
                                    data=json.dumps(self.REQUEST)
                                    )
        print(response.json())
        print("쿠팡API 연결 완료")

        pass

    #카테고리별 베스트 상품 상세 정보 선택
    def SelectBestCategory(self, category_code):

        # 현재 스크립트 파일의 경로를 가져옵니다.
        path =   os.path.dirname(__file__)
        current_directory = os.path.dirname(path)
        # 결과 폴더를 생성할 경로 설정 (현재 스크립트 파일의 위치를 기준으로)
        self.file_path = os.path.join(current_directory, 'result', datetime.now().strftime("%Y%m%d%H%M%S"))

        # 경로생성
        # file_path = '/result/' + datetime.now().strftime("%Y%m%d%H%M%S")
        CommonUtils.CreateFolder(self.file_path)

        try:
            category_info = self.Category.get(category_code)
            code, description = category_info

            Limit = 10
            #CategoryId = 1017

            #API 호출
            self.REQUEST_METHOD = "GET"
            self.URL = "/v2/providers/affiliate_open_api/apis/openapi/products/bestcategories/" +  category_code + "?limit=" + str(Limit)

            authorization = self.GetAuthorization()
            url = "{}{}".format(self.DOMAIN, self.URL)
            response = requests.request(method=self.REQUEST_METHOD, url=url, headers={"Authorization": authorization,
                                                                                      "Content-Type": "application/json;charset=UTF-8"})
            retdata = json.dumps(response.json(), indent=4).encode('utf-8')
            jsondata = json.loads(retdata)
            #print(jsondata['data'])

            # Pandas DataFrame으로 변환
            df = pd.DataFrame(jsondata['data'])
            #api 사용 횟수 초과 예외 출력

            CSVManager.WriteCsvFile(self.ConvertDataFrame(df), self.file_path + '/' + str(description))

        except OSError:
            print('Error: Creating directory. ')



    #카테고리별 베스트 상품 상세 정보
    def SelectAllBestCategory(self):


        for category_code, category_info in self.Category.items():
            # 카테고리 코드와 설명을 추출합니다.
            code, description = category_info

            Limit = 10
            #CategoryId = 1017

            #API 호출
            self.REQUEST_METHOD = "GET"
            self.URL = "/v2/providers/affiliate_open_api/apis/openapi/products/bestcategories/" +  category_code + "?limit=" + str(Limit)

            authorization = self.GetAuthorization()
            url = "{}{}".format(self.DOMAIN, self.URL)
            response = requests.request(method=self.REQUEST_METHOD, url=url, headers={"Authorization": authorization,
                                                                                      "Content-Type": "application/json;charset=UTF-8"})
            retdata = json.dumps(response.json(), indent=4).encode('utf-8')
            jsondata = json.loads(retdata)
            #print(jsondata['data'])

            # Pandas DataFrame으로 변환
            df = pd.DataFrame(jsondata['data'])
            #api 사용 횟수 초과 예외 출력


            # 모든 행과 열 표시
            # pd.set_option('display.max_columns', None)  # 모든 열 표시
            # pd.set_option('display.max_rows', None)  # 모든 행 표시

            # DataFrame 출력
            #print(df)

            CSVManager.WriteCsvFile(self.ConvertDataFrame(df), self.file_path + '/' + str(description))
        print("베스트 상품 상세 정보 조회 완료")

    # 쿠팡 상세 상품 정보 검색
    def Search(self):
        #변수 설정
        Keyword = "컴퓨터"
        Limit = 5

        #API 호출
        self.REQUEST_METHOD = "GET"
        self.URL = "/v2/providers/affiliate_open_api/apis/openapi/products/search?keyword=" + urllib.parse.quote(Keyword) + "&limit=" + str(Limit)

        authorization = self.GetAuthorization()
        url = "{}{}".format(self.DOMAIN, self.URL)
        response = requests.request(method=self.REQUEST_METHOD, url=url, headers={"Authorization": authorization,
                                                                             "Content-Type": "application/json;charset=UTF-8"})
        retdata = json.dumps(response.json(), indent=4).encode('utf-8')
        jsondata = json.loads(retdata)
        data = jsondata['data']
        productdata = data['productData']
        print(data)
        print(productdata)
        print("검색결과 조회 완료")


        pass

    # 링크 생성
    def DeepLink(self, productUrl):
        # 웹 페이지로 이동
        self.DRIVER.get(productUrl)
        # 원본 주소 가져오기
        original_link = self.DRIVER.current_url

        # API 호출
        self.REQUEST_METHOD = "POST"
        self.URL = "/v2/providers/affiliate_open_api/apis/openapi/v1/deeplink"
        self.REQUEST = {"coupangUrls": [original_link]}

        authorization = self.GetAuthorization()
        url = "{}{}".format(self.DOMAIN, self.URL)
        response = requests.request(method=self.REQUEST_METHOD, url=url,
                                    headers={
                                        "Authorization": authorization,
                                        "Content-Type": "application/json"
                                    },
                                    data=json.dumps(self.REQUEST)
                                    )

        #print(response.json())
        shorten_urls = str([item['shortenUrl'] for item in response.json()['data']])
        #print(str(shorten_urls))
        #print("단축 링크 생성 완료")
        return shorten_urls

    def ConvertDataFrame(self,df):

        # 새로운 데이터프레임을 생성합니다.
        new_df = pd.DataFrame(
            columns=[ 'rank', 'productId', 'productName', 'productPrice', 'productImage', 'categoryName', 'keyword','productUrl','shortUrl'])

        for index, row in df.iterrows():

            # 각 행의 데이터를 새로운 데이터프레임에 추가합니다.
            new_row = {
                #'index': index,
                'rank': row['rank'],
                'productId': row['productId'],
                'productName': row['productName'],
                'productPrice': row['productPrice'],
                'productImage': row['productImage'],
                'categoryName': row['categoryName'],
                'keyword': row['keyword'],
                'productUrl': str(row['productUrl']),
                'shortUrl': self.DeepLink(row['productUrl'])

            }

            new_df = pd.concat([new_df, pd.DataFrame([new_row])], ignore_index=True)

        return new_df


    def GetImage(self, imgurl):
        value = imgurl  # 이미지 가져오기

        # 현재 스크립트 파일의 경로를 얻습니다.
        script_dir = os.path.dirname(__file__)

        # res 폴더의 부모 디렉토리로 이동하여 이미지 파일의 상대 경로 설정
        image_path = os.path.join(script_dir, '..', 'res', 'Template1.png')

        # 이미지 파일을 불러오기
        background_image = cv2.imread(image_path)

        # 이미지 다운로드
        response = requests.get(value)

        if response.status_code == 200:
            # 이미지를 바이트 데이터로 변환
            image_data = BytesIO(response.content)
            # 바이트 데이터를 NumPy 배열로 변환
            np_array = np.frombuffer(image_data.read(), np.uint8)
            # OpenCV로 이미지 읽기
            insert_image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
            insert_image = cv2.resize(insert_image, (1000, 900))

            insert_height, insert_width, _ = insert_image.shape
            background_height, background_width, _ = background_image.shape

            # 삽입할 이미지가 배경 이미지의 특정 위치에 들어가게 조정합니다.
            x_position = 800  # 삽입 위치의 x 좌표
            y_position = 100  # 삽입 위치의 y 좌표

            # 삽입할 이미지를 배경 이미지에 복사합니다.
            background_image[y_position:y_position + insert_height, x_position:x_position + insert_width] = insert_image

            # 이미지를 다시 OpenCV 형식으로 변환
            # background_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        return background_image
        # 이미지 바로 보는 용도
        # plt.imshow(cv2.cvtColor(background_image, cv2.COLOR_BGR2RGB))
        # plt.show()

    def CreateImage(self):

        root = tk.Tk()
        root.withdraw()  # tkinter 창 숨기기

        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        # 이미지를 저장할 디렉토리 경로 추출
        output_directory = os.path.dirname(file_path)

        if file_path:

            csv = CSVManager.ReadCsvFile(file_path)

            for index, row in csv.iterrows():
                TemplateImage = self.GetImage(row['5'])

                # Pillow를 사용하여 이미지에 텍스트 추가
                image = Image.fromarray(cv2.cvtColor(TemplateImage, cv2.COLOR_BGR2RGB))
                draw = ImageDraw.Draw(image)

                # 현재 스크립트 파일의 경로를 얻습니다.
                script_dir = os.path.dirname(__file__)

                # res 폴더의 부모 디렉토리로 이동하여 이미지 파일의 상대 경로 설정
                fonts_path = os.path.join(script_dir, '..', 'fonts')

                text = str(row['3'])
                formatted_text = ''
                word = ''

                for char in text:
                    if char == ' ':
                        if len(word) >= 10:
                            formatted_text += '\n'
                        formatted_text += word + ' '
                        word = ''
                    else:
                        word += char

                if len(word) >= 10:
                    formatted_text += '\n'
                formatted_text += word

                # 텍스트를 추가할 위치와 내용을 리스트로 정의
                text_info_list = [
                    # 랭킹
                    {'text': str(row['1']) + '위',
                     'position': (80,360),
                     'font': os.path.join(fonts_path, 'GmarketSansTTFBold.ttf'),
                     'font-size': 180,
                     'font-color': 'black'
                    },
                    # 제품명
                    {'text': str(row['3']),
                     'position': (100, 620),
                     'font': os.path.join(fonts_path, 'GmarketSansTTFBold.ttf'),
                     'font-size': 70,
                     'font-color': '#00FE67'
                     },
                    # 가격
                    {'text': str(row['4']) + '원',
                     'position': (100, 880),
                     'font': os.path.join(fonts_path, 'GmarketSansTTFBold.ttf'),
                     'font-size': 100,
                     'font-color': '#363D62'
                     },
                    # 카테고리
                    {'text': str(row['6']) ,
                     'position': (80, 50),
                     'font': os.path.join(fonts_path, 'GmarketSansTTFBold.ttf'),
                     'font-size': 110,
                     'font-color': '#363D62'
                     },
                ]

                # 모든 텍스트 추가
                for text_info in text_info_list:
                    text = text_info['text']
                    position = text_info['position']
                    font = ImageFont.truetype(text_info['font'], text_info['font-size'])
                    draw.text(position, text, fill=text_info['font-color'], font=font)

                # 이미지를 다시 OpenCV 형식으로 변환
                TemplateImage = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

                # 이미지 저장 파일명 및 경로 설정
                output_image_path = os.path.join(output_directory, f"output_{index}.png")
                # 이미지 저장
                cv2.imwrite(output_image_path, TemplateImage)

    def CreateVideo(self):
        root = tk.Tk()
        root.withdraw()  # Tk 창 숨기기

        folder_selected = filedialog.askdirectory()  # 폴더 선택기 열기

        if folder_selected:
            # 현재 스크립트 파일의 경로를 얻습니다.
            script_dir = os.path.dirname(__file__)
            # res 폴더의 부모 디렉토리로 이동하여 intro.mp4 파일의 전체 경로 설정
            intro_path = os.path.join(script_dir, '..', 'res', 'intro.mp4')
            bgm_path = os.path.join(script_dir, '..', 'res', 'bgm.mp3')

            image_folder = folder_selected
            video_name = os.path.join(image_folder, 'video.avi')

            # intro.mp4 파일을 읽어와서 동영상 객체 생성
            intro_video = cv2.VideoCapture(intro_path)
            intro_frame_rate = int(intro_video.get(cv2.CAP_PROP_FPS))
            intro_frame_width = int(intro_video.get(cv2.CAP_PROP_FRAME_WIDTH))
            intro_frame_height = int(intro_video.get(cv2.CAP_PROP_FRAME_HEIGHT))

            # 비디오 생성을 위한 VideoWriter 설정
            fourcc = cv2.VideoWriter_fourcc(*'DIVX')
            video = cv2.VideoWriter(video_name, fourcc, intro_frame_rate, (intro_frame_width, intro_frame_height))

            # intro.mp4 파일 프레임 추가
            while True:
                ret, frame = intro_video.read()
                if not ret:
                    break
                video.write(frame)

            # 이미지 폴더에서 이미지 목록을 가져옵니다.
            images = [img for img in os.listdir(image_folder) if img.endswith(".jpg") or img.endswith(".png")]

            if len(images) > 0:
                # 각 이미지를 읽어서 비디오에 추가합니다. (각 이미지를 6초 동안 표시)
                for image in reversed(images):
                    img_path = os.path.join(image_folder, image)
                    img = cv2.imread(img_path)

                    # 이미지를 6초 동안 프레임으로 추가
                    for _ in range(6 * intro_frame_rate):
                        video.write(img)

                print("비디오 생성이 완료되었습니다.")
            else:
                print("폴더에 이미지 파일이 없습니다.")

            # 비디오 라이터를 해제합니다.
            video.release()
            intro_video.release()

            # BGM을 추가하여 새로운 동영상 생성
            output_video_path = os.path.join(image_folder, 'resuit.mp4')
            self.add_bgm_to_video(video_name, bgm_path, output_video_path)
        else:
            print("폴더를 선택하지 않았습니다.")

    def add_bgm_to_video(self, video_path, bgm_path, output_path):
        video_clip = VideoFileClip(video_path)
        bgm_clip = AudioFileClip(bgm_path)

        # 비디오와 BGM을 합성하여 새로운 비디오 클립 생성
        final_clip = video_clip.set_audio(bgm_clip)

        # 새로운 동영상 파일로 저장
        final_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')




