import hmac
import hashlib
import requests
import json
from time import gmtime, strftime
import urllib.request
from urllib.parse import urlencode
from Common.CommonAPI import CommonAPI


class CoupangAPI(CommonAPI):

    REQUEST_METHOD = None
    DOMAIN = "https://api-gateway.coupang.com"
    URL = None
    REQUEST = None
    # Replace with your own ACCESS_KEY and SECRET_KEY
    ACCESS_KEY = "9a6f6be2-96ff-4a2a-9c50-e16262589987"
    SECRET_KEY = "ac68c2ba170e765c2dd548a2a0dfab6d48a87377"
    _instance = None  # 클래스 레벨에서 정적 변수로 선언

    def __init__(self):
        self.Initialize()
        # pass

    @staticmethod
    def GetInstance():
        if CoupangAPI._instance is None:  # 인스턴스가 아직 없으면 생성
            CoupangAPI._instance = CoupangAPI()
        return CoupangAPI._instance

    def Initialize(self):
        self.ConnectAPI()
        print("쿠팡API 초기화 완료")
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
        self.Search()
        pass

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



        # API 호출
        self.REQUEST_METHOD = "POST"
        self.URL = "/v2/providers/affiliate_open_api/apis/openapi/v1/deeplink"
        self.REQUEST = {
                        "coupangUrls": [
                            "https://www.coupang.com/vp/products/7342370420?itemId=18874812284&vendorItemId=81729017725&src=1139000&spec=10799999&addtag=400&ctag=7342370420&lptag=AF9851400&itime=20231010003236&pageType=PRODUCT&pageValue=7342370420&wPcid=16968599974922541108147&wRef=&wTime=20231010003236&redirect=landing&traceid=V0-153-0414743331375bbd&mcid=a52dcf7b1b9e45c78af7f190dce5a6b8&placementid=&clickBeacon=&campaignid=&contentcategory=&imgsize=&tsource=&pageid=&deviceid=&token=31850C%7CMIXED&contenttype=&subid=&impressionid=&campaigntype=&requestid=20231010003211832262124933&contentkeyword=&subparam=&isAddedCart="
                        ]
                        }

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
        print("링크 조회 완료")
        pass