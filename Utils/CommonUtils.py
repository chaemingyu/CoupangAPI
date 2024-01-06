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