import mysql
import requests
import json
import db


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

data = []
sql = "INSERT INTO champion (`key`, name, english_name, detail, type, consume_type, is_active) VALUES (%s, %s, %s, %s, %s, %s, %s)"

for c in champion_data:
    data.append((c.key, c.name, c.english_name, c.detail, ', '.join(c.type), c.consume_type, 1))


for d in data:
    print(d)

try:
    # executemany() 메서드를 사용하여 여러 개의 데이터를 한 번에 삽입
    for item in data:
        # 데이터 하나씩 삽입
        db.cur.execute(sql, item)

    # 변경사항을 커밋
    db.db.commit()

except mysql.connector.Error as err:
    print("오류 발생:", err)
    db.db.rollback()

finally:
    # 연결과 커서 종료
    db.cur.close()
    db.db.close()
