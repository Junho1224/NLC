import pandas as pd
from pymongo import MongoClient

# CSV 파일 읽기
df = pd.read_csv('./dataNop/apartment.csv', encoding='utf-8')
df2 = pd.read_csv('./dataNop/officetel.csv', encoding='utf-8')

# MongoDB 클라이언트 설정
username = 'root'  # 실제 MongoDB 사용자 이름
password = 'root'  # 실제 MongoDB 사용자 비밀번호
client = MongoClient(f'mongodb://{username}:{password}@175.106.97.107:27017/')
db = client['mongo_db']  # 데이터베이스 이름 설정
apartments_lands = db['apartments']  # 컬렉션 이름 설정
officetels_lands = db['officetels']  # 컬렉션 이름 설정

# Apartment 데이터 삽입
lands_data = df.to_dict(orient='records')
apartments_lands.insert_many(lands_data)


# Officetel 데이터 삽입
lands_data = df.to_dict(orient='records')
officetels_lands.insert_many(lands_data)


print("Data inserted successfully into MongoDB")