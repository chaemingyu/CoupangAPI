import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import Common
from Core.CoupangAPI import CoupangAPI  # Core 패키지 내의 CoupangAPI 모듈을 가져옵니다.
from Core.YoutubeAPI import YoutubeAPI  # Core 패키지 내의 YoutubeAPI 모듈을 가져옵니다.
import tkinter as tk
from tkinter import filedialog
class MainWindow(QMainWindow):

    category = None

    def __init__(self):
        super().__init__()

        loadUi('C:/fork/CoupangAPI/mainwindow.ui', self)
        self.inibtn.clicked.connect(self.IniBtnClick)
        self.searchbtn.clicked.connect(self.SerachBtnClick)
        self.createimagbtn.clicked.connect(self.CreateImgBtnClick)
        self.createvideobtn.clicked.connect(self.CreateVideoBtnClick)

        self.createscrpitbtn.clicked.connect(self.CreateScriptBtnClick)

        self.youtubeuploadbtn.clicked.connect(self.YouubeUploadBtnClick)


        # QTextEdit 위젯 생성
        self.log.setReadOnly(True)  # 읽기 전용 모드로 설정하여 사용자 입력 방지
        self.log.setFontFamily("Courier")  # 특정 폰트로 설정 (예: Courier)


        self.ShoppingCategorymodel = QStandardItemModel()

        # Column Names
        column_names = ["Key", "영문 카테고리", "한글 카테고리"]

        # Set Column Headers

        self.ShoppingCategorymodel.setHorizontalHeaderLabels(column_names)
        # ShoppingCategory 딕셔너리 순회하며 모델에 아이템 추가
        for key, value in Common.Config.ShoppingCategory.items():
            key_item = QStandardItem(str(key))  # key
            value_0_item = QStandardItem(str(value[0]))  # value[0]\
            value_1_item = QStandardItem(str(value[1]))  # value[1]

            # 모델에 각 항목을 추가
            self.ShoppingCategorymodel.appendRow([key_item, value_0_item, value_1_item])
            # self.ShoppingCategorymodel.appendRow( value_0_item)
            # self.ShoppingCategorymodel.appendRow(value_1_item)

        self.shoppingtableView.setModel(self.ShoppingCategorymodel)
        # self.tableView.setModel(self.ShoppingCategorymodel)

        # 리스트뷰의 아이템 클릭 이벤트 핸들러 연결
        self.shoppingtableView.clicked.connect(self.onTableClicked)

        self.coupang = CoupangAPI.GetInstance()
        self.youtube = YoutubeAPI.GetInstance()

    def IniBtnClick(self):

        self.coupang.Initialize()
        self.Append_log("쿠팡API 초기화 완료")
        # print("쿠팡API 초기화 완료")
        pass

    def SerachBtnClick(self):
        if self.category is not None:
            cell_text = self.category.text()  # 클릭된 셀의 텍스트 가져오기
            # print(f"Clicked row: {row}, column: {column}, value: {cell_text}")

        self.coupang.SelectBestCategory(cell_text)
        self.Append_log("조회 완료")
        #self.coupang.ConnectAPI()
        pass

    def Append_log(self, log):
        # 로그 텍스트를 추가하는 메서드
        self.log.append(log)

    # 리스트뷰 클릭 이벤트 핸들러
    def onTableClicked(self, index):
        row = index.row()  # 클릭된 행의 인덱스 가져오기
        column = 0  # 클릭된 열의 인덱스 가져오기

        self.category = self.ShoppingCategorymodel.item(row, column)  # 클릭된 셀의 아이템 가져오기

    def CreateImgBtnClick(self):
        self.coupang.CreateImage()
        self.Append_log("이미지 생성 완료")
        pass

    def CreateScriptBtnClick(self):
        root = tk.Tk()
        root.withdraw()  # tkinter 창 숨기기

        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        # 이미지를 저장할 디렉토리 경로 추출

        self.youtube.CreateScript(file_path)
        #설명 생성
        self.youtube.CreateDescription(file_path)
        self.Append_log("스크립트 생성 완료")
        pass

    def CreateVideoBtnClick(self):
        self.coupang.CreateVideo()
        self.Append_log("동영상 생성 완료")
        pass

    def YouubeUploadBtnClick(self):
        root = tk.Tk()
        root.withdraw()  # tkinter 창 숨기기

        file_path = filedialog.askopenfilename()

        self.youtube.UploadVideo(file_path)
        self.Append_log("유튜브 업로드 완료")
        pass


if __name__ == "__main__":
    # coupang = CoupangAPI.GetInstance()
    # coupang.ConnectAPI()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()


