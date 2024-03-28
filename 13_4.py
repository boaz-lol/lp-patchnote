import requests
from bs4 import BeautifulSoup, Tag
import json


class Item(object):
    def __init__(self, detail, before, after):
        self.detail = detail
        self.before = before
        self.after = after

    def __dict__(self):
        return {
            'detail': self.detail,
            'before': self.before,
            'after': self.after
        }


class Update(object):
    def __init__(self, type):
        self.type = type
        self.items = []

    def __add__(self, item):
        self.items.append(item)

    def __dict__(self):
        return {
            'type': self.type,
            'items': [item.__dict__() for item in self.items]
        }


class Champion(object):
    def __init__(self):
        self.name = ""
        self.type = ""
        self.updates = []

    def __set_name__(self, name):
        self.name = name

    def __add__(self, update):
        self.updates.append(update)

    def __set_type__(self, type):
        self.type = type

    def __dict__(self):
        return {
            'name': self.name,
            'type': self.type,
            'updates': [update.__dict__() for update in self.updates]
        }


URL = 'https://www.leagueoflegends.com/ko-kr/news/game-updates/patch-{v}-notes/#patch-champions'


version = [
    "13-4"
]

for x in range(len(version)):
    response = requests.get(URL.format(v=version[x]))
    print(version[x], response)
    update_list = []
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        container = soup.select_one('#gatsby-focus-wrapper > div > section > section.style__Wrapper-sc-17x3yhp-0.style__ResponsiveWrapper-sc-17x3yhp-10.gLXFgp.izJRkJ > div')
        print(container)
        champions = []
        isStarted = False
        for c in container:
            if c.name == 'header':
                if c.select_one('h2').text == '챔피언':
                    isStarted = True
                else:
                    isStarted = False

            if isStarted and isinstance(c, Tag):
                champions.append(c)

        for c in champions:
            new = Champion()
            updated_ul = []
            updated_li = []

            if c.select_one('h3'):
                # 챔피언 이름
                champ = c.select_one('h3').find('a')
                name = ""
                update_type = ""
                for child in champ.contents:
                    if child.name == 'span':
                        update_type = str(child)
                    if not child.name == 'span':
                        name += str(child)

                new.__set_name__(name)
                new.__set_type__(update_type)

                # 챔피언 업데이트 스텟
                for title in c.select('h4'):
                    updated_ul.append(title.text)

                for ul in c.select('ul'):
                    tmp = []
                    for li in ul.select('li'):
                        if ":" not in li.text:
                            continue
                        item, modified = li.text.split(": ", 1)
                        before, after = "", ""
                        if " ⇒ " in modified:
                            before, after = modified.split(" ⇒ ", 1)
                        else:
                            after = modified
                        tmp.append([item, before, after])
                    updated_li.append(tmp)
            else:
                continue

            for i in range(len(updated_ul)):
                update = Update(updated_ul[i])
                for l in updated_li[i]:
                    update.__add__(Item(l[0], l[1], l[2]))

                new.__add__(update)

            update_list.append(new.__dict__())
    file_path = "./champion_init/{version}.json"
    with open(file_path.format(version=version[x]), 'w', encoding='utf-8') as file:
        json.dump(update_list, file, indent="\t", ensure_ascii=False)


