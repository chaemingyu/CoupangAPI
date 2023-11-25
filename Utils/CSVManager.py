import pandas as pd

def ReadCsvFile():
    df = pd.read_csv('Test.csv')  # 파일이 저장된 경로 입력

    header = True  # header를 출력할 경우
    index = True  # index를 출력할 경우
    sep = ','  # 구분자 기호 넣을 경우 default는 ','
    encoding = 'utf-8'  # 한글 깨질 경우 인코딩에 맞게 입력
    return df

def WriteCsvFile(df, title):

    pd.DataFrame(df).to_csv(title +'.csv', header=False, index=False, encoding='cp949')

    pass
