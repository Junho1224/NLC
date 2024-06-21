import pandas as pd
from sqlalchemy.orm import Session
from database import engine
import models

# CSV 파일 읽기
df = pd.read_csv('GangnamALL.csv',encoding='utf-8')
df1 = pd.read_csv('GangnamAdd.csv',encoding='utf-8')

# 데이터베이스 세션 생성
session = Session(bind=engine)

# 데이터베이스에 데이터 삽입
for index, row in df.iterrows():
    land = models.Lands(
        area=row['area'],
        atclNo=row['atclNo'],
        atclNm=row['atclNm'],
        rletTpNm=row['rletTpNm'],
        tradTpNm=row['tradTpNm'],
        flrInfo=row['flrInfo'],
        prc=row['prc'],
        rentPrc=row['rentPrc'],
        hanPrc=row['hanPrc'],
        spc1=row['spc1'],
        spc2=row['spc2'],
        direction=row['direction'],
        atclCfmYmd=row['atclCfmYmd'],
        atclFetrDesc=row['atclFetrDesc'],
        tagList=row['tagList'],
        bildNm=row['bildNm'],
        
    )
    session.add(land)
    
session.commit()
session.close()


for index, row in df1.iterrows():
    land_add = models.LandsAdd(
        area=row['area'],
        lat=row['lat'],
        lng=row['lng'],
        road_address=row['road_address'],
        address=row['address']
    )
    session.add(land_add)

session.commit()
session.close()