import sys
from Core.CoupangAPI import CoupangAPI  # Core 패키지 내의 CoupangAPI 모듈을 가져옵니다.
from PyQt5.QtWidgets import *

# class MyWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#
#         self.Initialize()
#
#         self.setGeometry(500, 500, 400, 300)
#
#         ConnectCounpangAPI = QPushButton(text="테스트", parent=self)
#         ConnectCounpangAPI.move(10, 10)
#         ConnectCounpangAPI.resize(150,30)
#         ConnectCounpangAPI.clicked.connect(self.ConnectAPI)
#
#     def Initialize(self):
#         self.coupang = CoupangAPI.GetInstance()
#
#     def ConnectAPI(self):
#         try:
#             self.coupang.ConnectAPI()
#             #print(ConnectAPI(coupang))
#         except Exception as e:
#             QMessageBox.about(self, '에러', str(e))

coupang = None
if __name__ == "__main__":
    coupang = CoupangAPI.GetInstance()
    coupang.ConnectAPI()

    # app = QApplication(sys.argv)
    # window = MyWindow()
    # window.show()
    # app.exec_()