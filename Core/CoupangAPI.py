import hmac
import hashlib
import requests
import json
from time import gmtime, strftime
from Common.CommonAPI import CommonAPI


class CoupangAPI(CommonAPI):
    _instance = None  # 클래스 레벨에서 정적 변수로 선언

    #HMAC 서명 생성 및 API 호출
    REQUEST_METHOD = "POST"
    DOMAIN = "https://api-gateway.coupang.com"
    URL = "/v2/providers/affiliate_open_api/apis/openapi/v1/deeplink"

    # Replace with your own ACCESS_KEY and SECRET_KEY
    ACCESS_KEY = "9a6f6be2-96ff-4a2a-9c50-e16262589987"
    SECRET_KEY = "ac68c2ba170e765c2dd548a2a0dfab6d48a87377"

    REQUEST = {"coupangUrls": [
        "https://www.coupang.com/np/search?component=&q=good&channel=user",
        "https://www.coupang.com/np/coupangglobal"
    ]}

    def __init__(self):
        self.Initialize()
        # pass

    def Initialize(self):
        print("쿠팡 초기화")
        pass

    @staticmethod
    def GetInstance():
        if CoupangAPI._instance is None:  # 인스턴스가 아직 없으면 생성
            CoupangAPI._instance = CoupangAPI()
        return CoupangAPI._instance
    
    def ConnectAPI(self):
        authorization = self.generateHmac(self.REQUEST_METHOD, self.URL, self.SECRET_KEY, self.ACCESS_KEY)
        url = "{}{}".format(self.DOMAIN, self.URL)
        response = requests.request(method=self.REQUEST_METHOD, url=url,
                                    headers={
                                        "Authorization": authorization,
                                        "Content-Type": "application/json"
                                    },
                                    data=json.dumps(self.REQUEST)
                                    )

        print(response.json())

        print("쿠팡 연결")
        pass

    def generateHmac(self,method, url, secretKey, accessKey):
        path, *query = url.split("?")
        datetimeGMT = strftime('%y%m%d', gmtime()) + 'T' + strftime('%H%M%S', gmtime()) + 'Z'
        message = datetimeGMT + method + path + (query[0] if query else "")

        signature = hmac.new(bytes(secretKey, "utf-8"),
                             message.encode("utf-8"),
                             hashlib.sha256).hexdigest()

        return "CEA algorithm=HmacSHA256, access-key={}, signed-date={}, signature={}".format(accessKey, datetimeGMT, signature)