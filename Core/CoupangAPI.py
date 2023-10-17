import hmac
import hashlib
import requests
import json
from time import gmtime, strftime
import urllib.request
from urllib.parse import urlencode
from Common.CommonAPI import CommonAPI

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import pandas as pd
import pixabay.core
from Utils import CSV

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

    Category = {
        "1001" : ["woman","여성패션"],
        "1002": ["Man", "남성패션"],
        "1010": ["beauty", "뷰티"],
        "1011": ["child", "출산_유아동"],
        "1012": ["food", "식품"],
        "1013": ["Kitchenware", "주방용품"],
        "1014": ["Daily Necessity", "생활용품"],
        "1015": ["home interior", "홈인테리어"],
        "1016": ["home appliances", "가전디지털"],
        "1017": ["sports", "스포츠_레저"],
        "1018": ["vehicle supplies", "자동차용품"],
        "1019": ["book", "도서_음반_DVD"],
        "1020": ["Hobby", "완구_취미"],
        "1021": ["office supplies", "문구_오피스"],
        "1024": ["health", "헬스_건강식품"],
        "1025": ["domestic travel", "국내여행"],
        "1026": ["Overseas Travel", "해외여행"],
        "1029": ["pet products", "반려동물용품"],
        "1030": ["infant fashion", "유아동패션"],
    }
    def __init__(self):
        self.Initialize()
        # pass

    @staticmethod
    def GetInstance():
        if CoupangAPI._instance is None:  # 인스턴스가 아직 없으면 생성
            CoupangAPI._instance = CoupangAPI()
        return CoupangAPI._instance

    def Initialize(self):
        #self.ConnectAPI()

        # Chrome 옵션 초기화
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # 브라우저를 표시하지 않고 백그라운드에서 실행

        # Chrome 웹 드라이버 초기화
        self.DRIVER = webdriver.Chrome(options=chrome_options)

        print("쿠팡API 초기화 완료")

        self.BestCategory()

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
        # self.REQUEST_METHOD = "POST"
        # self.URL = "/v2/providers/affiliate_open_api/apis/openapi/v1/deeplink"
        #
        # self.REQUEST = {"coupangUrls": [
        #     "https://www.coupang.com/np/search?component=&q=good&channel=user",
        #     "https://www.coupang.com/np/coupangglobal"
        # ]}
        #
        # authorization = self.GetAuthorization()
        # url = "{}{}".format(self.DOMAIN, self.URL)
        # response = requests.request(method=self.REQUEST_METHOD, url=url,
        #                             headers={
        #                                 "Authorization": authorization,
        #                                 "Content-Type": "application/json"
        #                             },
        #                             data=json.dumps(self.REQUEST)
        #                             )
        # print(response.json())
        print("쿠팡API 연결 완료")

        pass

    #카테고리별 베스트 상품 상세 정보
    def BestCategory(self):

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
            pd.set_option('display.max_columns', None)  # 모든 열 표시
            pd.set_option('display.max_rows', None)  # 모든 행 표시

            # DataFrame 출력
            #print(df)
            CSV.WriteCsvFile(self.ConvertDataFrame(df), str(description))

        # 위에서 DataFrame을 생성한 후
        #for index, row in df.iterrows():

            # print("Index:", index)
            # print("rank:", row['rank'] )
            # print("productId:", row['productId'])
            # print("productName:", row['productName'])
            # print("productPrice:", row['productPrice'])
            # print("productImage:", row['productImage'])
            # print("categoryName:", row['categoryName'])
            # print("keyword:", row['keyword'])
            # print("productUrl:", str(row['productUrl']))
            #self.DeepLink(row['productUrl'])
            #Utill.GetSumnail(row['keyword'])

            # # 키입력
            # API_KEY = '40053999-2b85d1718a7ec3f2d658c6ade'
            # # 발급 받은 API 키를 입력한다.
            # px = pixabay.core(API_KEY)
            # image = px.query('sports')
            #
            # # 몇 개 검색했는지 나옴
            # print("{} hits".format(len(image)))
            #
            # # 첫 번째 인덱스의 이미지를 다운로드 함.
            # image[index].download("TEST"+ str(index) + ".jpg", "largeImage")

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