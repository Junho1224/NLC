import pandas as pd
from sqlalchemy.orm import Session
from database import engine
import models

# CSV 파일 읽기
df = pd.read_csv('양천구_신월동_100.csv',encoding='utf-8')

# 데이터베이스 세션 생성
session = Session(bind=engine)

# 데이터베이스에 데이터 삽입
for index, row in df.iterrows():
    land = models.Lands(
        atclNo=row['atclNo'],
        atclNm=row['atclNm'],
        rletTpNm=row['rletTpNm'],
        prc=row['prc'],
        lat=row['lat'],
        lng=row['lng']
    )
    session.add(land)

# 커밋 및 세션 종료
session.commit()
session.close()