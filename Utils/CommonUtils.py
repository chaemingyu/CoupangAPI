import os
import csv

# 디렉토리생성
def CreateFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)


# CSV 파일로 저장하기
def save_to_csv(data, file_path):
    with open(file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=data.keys())
        writer.writeheader()
        writer.writerow(data)

# CSV 파일에서 읽어오기
def read_from_csv(file_path):
    with open(file_path, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        data = next(reader)  # 첫 번째 행 가져오기
    return data


#텍스트 파일 생성
def SaveTextFile(text, output_file_path):
    # 스크립트 템플릿을 파일로 저장
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(text)


# 텍스트 파일 읽기 함수 정의
def ReadTextFile( file_path):
    # 파일에서 텍스트 읽기
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            return text
    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")
        return None