import pandas as pd
import os
def ReadCsvFile(file_path):
    # file_path = r'D:\CoupangAPI\result\20231125171008\여성패션.csv'

    # file_path = os.path.join(file_path, '여성패션.csv')
    df = pd.read_csv(file_path, encoding='cp949', names = ['1','2','3','4','5','6','7','8','9'])
    #header =True #header를 출력할 경우
    #index = True #index를 출력할 경우
    #sep=',' #구분자 기호 넣을 경우 default는 ','
    #encoding='utf-8' #한글 깨질 경우 인코딩에 맞게 입력
    return df

def WriteCsvFile(df, title):

    pd.DataFrame(df).to_csv(title +'.csv', header=False, index=False, encoding='cp949')

    pass
