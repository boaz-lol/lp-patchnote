"""
https://ddragon.leagueoflegends.com/cdn/12.1.1/data/ko_KR/champion/Aatrox.json

12.1 버전을 챔피언 초기값으로 데이터를 패치하는 코드
"""

import requests
import json

champions = requests.get("https://ddragon.leagueoflegends.com/cdn/13.1.1/data/ko_KR/champion.json").json()["data"]

for c in champions:
    print(champions[c])


champion_datail_url = "https://ddragon.leagueoflegends.com/cdn/13.1.1/data/ko_KR/champion/{name}.json"
file_path = "./champion_init/{name}.json"

for c in champions:
    data = requests.get(champion_datail_url.format(name=c)).json()
    print(data)
    with open(file_path.format(name=c), 'w', encoding='utf-8') as file:
        json.dump(data, file, indent="\t", ensure_ascii=False)
