import requests
import json


class Champion(object):
    def __init__(self, name, english_name, key, detail, type, consume_type):
        self.name = name
        self.english_name = english_name
        self.key = key
        self.detail = detail
        self.type = type
        self.consume_type = consume_type


champions = requests.get("https://ddragon.leagueoflegends.com/cdn/14.8.1/data/ko_KR/champion.json").json()["data"]
champion_data = []

for c in champions:
    champion = champions[c]
    if champion["key"] == "200":
        print(champion)
    champion_data.append(Champion(
        name=champion["name"],
        english_name=champion["id"],
        key=champion["key"],
        detail=champion["blurb"],
        type=champion["tags"],
        consume_type=champion["partype"]
    ))

for c in champion_data:
    print(c.name)
    print(c.key)
    print(c.detail)
    print(c.type)
    print(c.consume_type)
    print("------------------------")