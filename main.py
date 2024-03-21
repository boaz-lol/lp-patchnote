"""
정기적으로 ETL을 수행하는 패치노트
"""

import requests
from bs4 import BeautifulSoup, Tag

class Updated(object):
    def __init__(self):
        self.type = ""
        self.detail = ""
        self.before = ""
        self.after = ""

class Champion(object):
    def __init__ (self):
        self.name = ""
        self.update = []
    

url = 'https://www.leagueoflegends.com/ko-kr/news/game-updates/patch-14-4-notes/#patch-champions'

response = requests.get(url)

if response.status_code == 200:
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    container = soup.select_one('#patch-notes-container')
    
    champions = []
    isStarted = False
    for c in container:
        if c.name == 'header':
            if c.select_one('h2').text == '챔피언': isStarted = True
            else: isStarted = False

        if isStarted == True and isinstance(c, Tag):
            champions.append(c)

    for c in champions:
        new = Champion()
        updated_ul = []
        updated_li = []
        
        if c.select_one('h3'):
            # 챔피언 이름
            new.name = c.select_one('h3').find('a').text
            print(new.name)
            
            # 
            for title in c.select('h4'):
                updated_ul.append(title.text)
            
            for ul in c.select('ul'):
                tmp = []
                for li in ul.select('li'):
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
            print(updated_ul[i])
            for l in updated_li[i]:
                print(l)
        
        print()
            
        
else: 
    print(response.status_code)