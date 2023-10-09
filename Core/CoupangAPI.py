
from Common.CommonAPI import CommonAPI
#싱글톤 클래스
class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class CoupangAPI(metaclass=Singleton ):
    _instance = None  # 클래스 레벨에서 정적 변수로 선언

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
        print("쿠팡 연결")
        pass