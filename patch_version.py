import requests
from bs4 import BeautifulSoup

url = "https://www.leagueoflegends.com/ko-kr/news/tags/patch-notes/"

response = requests.get(url)

if response.status_code == 200:
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    ol = soup.select_one('#gatsby-focus-wrapper > div > div.style__Wrapper-sc-1ynvx8h-0.style__ResponsiveWrapper-sc'
                         '-1ynvx8h-6.bNRNtU.dzWqHp > div > '
                         'div.style__Wrapper-sc-106zuld-0.style__ResponsiveWrapper-sc-106zuld-4.enQqER.jYHLfd'
                         '.style__List-sc-1ynvx8h-3.qfKFn > div > ol')
    versions = ol.select('li > a > article > div.style__Info-sc-1h41bzo-6.eBtwVi > div > h2')
    # print(versions[0].get_text())
    for v in versions:
        print(v.get_text())