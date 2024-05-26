import json

data = [
    {"lat": 37.566826, "lng": 126.9786567, "title": "서울특별시청"},
    {"lat": 37.570081, "lng": 126.983714, "title": "종로구청"},
    {"lat": 37.576126, "lng": 126.985022, "title": "북촌 한옥마을"}
]

with open('../data/locations.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)