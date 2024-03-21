"""
정기적으로 ETL을 수행하는 패치노트
"""

import requests
from bs4 import BeautifulSoup, NavigableString, Tag

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
        name  = ""
        updated_list = []
        updated_detail = []
        if c.select_one('h3'):
            name = c.select_one('h3').find('a').text
            
            updated_list.append(c.select('h4').text)
            updated_detail.append(c.select('ul'))
            
            for title, detail in updated_list, updated_detail:
                print(title)
                print(detail)
            
        
else: 
    print(response.status_code)