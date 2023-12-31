import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import Common
from Core.CoupangAPI import CoupangAPI  # Core 패키지 내의 CoupangAPI 모듈을 가져옵니다.

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        loadUi('D:/CoupangAPI/mainwindow.ui', self)
        self.inibtn.clicked.connect(self.IniBtnClick)
        self.searchbtn.clicked.connect(self.SerachBtnClick)

        # QTextEdit 위젯 생성
        self.log.setReadOnly(True)  # 읽기 전용 모드로 설정하여 사용자 입력 방지
        self.log.setFontFamily("Courier")  # 특정 폰트로 설정 (예: Courier)


        self.ShoppingCategorymodel = QStandardItemModel()

        # ShoppingCategory 딕셔너리 순회하며 모델에 아이템 추가
        for key, value in Common.Config.ShoppingCategory.items():
            key_item = QStandardItem(str(key))  # key
            value_0_item = QStandardItem(str(value[0]))  # value[0]\
            value_1_item = QStandardItem(str(value[1]))  # value[1]

            # 모델에 각 항목을 추가
            self.ShoppingCategorymodel.appendRow([value_1_item, key_item, value_0_item])
            # self.ShoppingCategorymodel.appendRow( value_0_item)
            # self.ShoppingCategorymodel.appendRow(value_1_item)

        self.shoppinglistView.setModel(self.ShoppingCategorymodel)

    def IniBtnClick(self):
        self.coupang = CoupangAPI.GetInstance()
        self.Append_log("쿠팡API 초기화 완료")
        # print("쿠팡API 초기화 완료")
        pass

    def SerachBtnClick(self):
        self.coupang.SelectBestCategory("1001")
        #self.coupang.ConnectAPI()
        pass

    def Append_log(self, log):
        # 로그 텍스트를 추가하는 메서드
        self.log.append(log)

if __name__ == "__main__":
    # coupang = CoupangAPI.GetInstance()
    # coupang.ConnectAPI()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()


