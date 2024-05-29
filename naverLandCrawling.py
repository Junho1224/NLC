import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import math
import re




def calculate_bounding_box(lat, lon, zoom):
    # Earth's radius in meters
    R = 6378137
    # Approximate bounding box in meters for zoom level 14 (usually covers around 1km)
    bounding_box_half_side_length = 1000  # 1km / 2

    # Convert latitude and longitude from degrees to radians
    lat_rad = math.radians(lat)
    lon_rad = math.radians(lon)
    
    # Offset calculations
    lat_offset = (bounding_box_half_side_length / R) * (180 / math.pi)
    lon_offset = (bounding_box_half_side_length / (R * math.cos(lat_rad))) * (180 / math.pi)
    
    # Calculate bounding box coordinates
    btm = lat - lat_offset
    lft = lon - lon_offset
    top = lat + lat_offset
    rgt = lon + lon_offset
    
    return btm, lft, top, rgt



# 검색할 키워드
keyword = "양천구 신월동"

# 검색 URL
url = "https://m.land.naver.com/search/result/{}".format(keyword)

# 필요한 헤더 설정
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Referer': 'https://m.land.naver.com/'
}

# GET 요청을 보냅니다
res = requests.get(url, headers=headers)
res.raise_for_status()

# 응답 데이터를 HTML로 파싱합니다
soup = str(BeautifulSoup(res.text, 'lxml'))

# 필요한 값 추출
value = soup.split("filter: {")[1].split("}")[0].replace(" ","").replace("'","")

print(value)

lat = (float)(value.split("lat:")[1].split(",")[0])
lon = (float)(value.split("lon:")[1].split(",")[0])
z = (int)(value.split("z:")[1].split(",")[0])
cortarNo = value.split("cortarNo:")[1].split(",")[0]
rletTpCds = value.split("rletTpCds:")[1].split(",")[0]
tradTpCds = value.split("tradTpCds:")[1].split()[0]


btm, lft, top, rgt = calculate_bounding_box(lat, lon, z)
print(f"btm: {btm}, lft: {lft}, top: {top}, rgt: {rgt}")


# clusterList URL
clusterList_URL = "https://m.land.naver.com/cluster/clusterList?view=atcl&cortarNo={}&rletTpCd={}&tradTpCd={}&z={}&lat={}&lon={}&btm={}&lft={}&top={}&rgt={}"\
    .format(cortarNo, rletTpCds, tradTpCds, z, lat, lon, btm, lft, top, rgt)
print(clusterList_URL)

# clusterList URL로 GET 요청
res2 = requests.get(clusterList_URL, headers=headers)
res2.raise_for_status()

# print(res2.text)

# JSON 데이터를 파싱
try:
    data = res2.json()
    # print(json.dumps(data, indent=2, ensure_ascii=False))
except json.JSONDecodeError as e:
    print("JSON 데이터를 파싱할 수 없습니다:", e)
    print("응답 내용:", res2.text)
    
values = data['data']['ARTICLE']
# print(values)



# 결과를 저장할 리스트
result_list = []

# 큰 원으로 구성되어 있는 전체 매물그룹(values)을 load 하여 한 그룹씩 세부 쿼리 진행
for v in values:
    lgeo = v['lgeo']
    count = v['count']
    z2 = v['z']
    lat2 = v['lat']
    lon2 = v['lon']

    len_pages = math.ceil(count / 20) + 1
    for idx in range(1, len_pages):
        
        articleList_URL = "https://m.land.naver.com/cluster/ajax/articleList?""itemId={}&mapKey=&lgeo={}&showR0=&" \
               "rletTpCd={}&tradTpCd={}&z={}&lat={}&""lon={}&totCnt={}&cortarNo={}&page={}"\
            .format(lgeo, lgeo, rletTpCds, tradTpCds, z2, lat2, lon2, count,cortarNo, idx)
        # print(articleList_URL)
        res3 = requests.get(articleList_URL, headers=headers)
        res3.raise_for_status()
                
        try:
            data2 = res3.json()
            articles = data2['body']
            for article in articles:
                result_list.append(article)
        except json.JSONDecodeError as e:
            print("JSON 데이터를 파싱할 수 없습니다:", e)
            print("응답 내용:", res3.text)

# pandas DataFrame으로 변환
df = pd.DataFrame(result_list)

# CSV 파일로 저장
df.to_csv(f'{keyword}_list.csv', index=False, encoding='utf-8-sig')

print("CSV 파일로 저장되었습니다.")
            
        

