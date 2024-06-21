import pandas as pd
from pymongo import MongoClient

# CSV 파일 읽기
df = pd.read_csv('Apartment.csv', encoding='utf-8')
df1 = pd.read_csv('ApartmentAdd.csv', encoding='utf-8')
df2 = pd.read_csv('Officetel.csv', encoding='utf-8')
df3 = pd.read_csv('OfficetelAdd.csv', encoding='utf-8')

# MongoDB 클라이언트 설정
client = MongoClient('mongodb://175.106.97.107:27017/')
db = client['mongo_db']  # 데이터베이스 이름 설정
collection_lands = db['lands']  # 컬렉션 이름 설정
collection_lands_add = db['lands_add']  # 컬렉션 이름 설정

# Apartment 데이터 삽입
lands_data = df.to_dict(orient='records')
collection_lands.insert_many(lands_data)

# ApartmentAdd 데이터 삽입
lands_add_data = df1.to_dict(orient='records')
collection_lands_add.insert_many(lands_add_data)

# Officetel 데이터 삽입
lands_data = df.to_dict(orient='records')
collection_lands.insert_many(lands_data)

# OfficetelAdd 데이터 삽입
lands_add_data = df1.to_dict(orient='records')
collection_lands_add.insert_many(lands_add_data)

print("Data inserted successfully into MongoDB")