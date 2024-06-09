import json
import boto3
import botocore

import requests
from bs4 import BeautifulSoup, Tag
import csv
import re
import io
from datetime import datetime


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


BUCKET_NAME = '*'
DIR_NAME = '*'
FILE_NAME = '*'
KEY = DIR_NAME + FILE_NAME

s3 = boto3.resource('s3').meta.client


def lambda_handler(event, context):
    print(KEY)
    result_list = []

    s3_object = s3.get_object(Bucket=BUCKET_NAME, Key='version/patch.csv')
    object_content = s3_object['Body'].read().decode('utf-8')

    f = io.StringIO(object_content)
    reader = list(csv.DictReader(f))
    season = reader[-1]["season"]
    version = reader[-1]["version"]
    expect_version = str(int(version) + 1)
    subversion = reader[-1]["subversion"]

    subVersionUpdated = False
    mainVersionUpdated = False

    url = "https://www.leagueoflegends.com/ko-kr/news/tags/patch-notes/"
    response = requests.get(url)
    homepage_last_update_version_text = ""
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        div = soup.select_one('#news > div > div.grid-content > div')
        versions = div.select('a')
        homepage_last_update_version_text = versions[0].get('aria-label')

    homepage_last_update_version_text_list = homepage_last_update_version_text.split(" ")

    homepage_last_subversion = subversion
    if homepage_last_update_version_text_list[0][0] == '[':
        homepage_last_subversion = re.findall(r'\d+', homepage_last_update_version_text.split(" ")[0])
        if int(homepage_last_subversion[0]) > int(subversion):
            subVersionUpdated = True

    if "{season}.{version}".format(season=season, version=expect_version) in homepage_last_update_version_text:
        homepage_last_subversion = 0
        mainVersionUpdated = True

    patch_version = ""
    if subVersionUpdated:
        patch_version = "{season}-{version}".format(season=season, version=version)
    elif mainVersionUpdated:
        patch_version = "{season}-{version}".format(season=season, version=expect_version)

    if len(patch_version) != 0:
        patch_note_url = 'https://www.leagueoflegends.com/ko-kr/news/game-updates/patch-{v}-notes/#patch-champions'
        response = requests.get(patch_note_url.format(v=patch_version))
        update_list = []
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')

            container = soup.select_one('#patch-notes-container')

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

        json_content = json.dumps(update_list, indent="\t", ensure_ascii=False)
        json_key = "patchnotes/{version}-{sub}.json".format(version=patch_version, sub=homepage_last_subversion)
        s3.put_object(Bucket=BUCKET_NAME, Key=json_key, Body=json_content, ContentType='application/json')

        current_date = datetime.now().strftime('%Y-%m-%d')
        new_row = {
            "date": current_date,
            "season": season,
            "version": expect_version,
            "subversion": homepage_last_subversion
        }
        reader.append(new_row)

        # 수정된 CSV 내용을 메모리에 작성
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=reader[0].keys())
        writer.writeheader()
        writer.writerows(reader)

        s3.put_object(Bucket=BUCKET_NAME, Key='version/patch.csv', Body=output.getvalue(), ContentType='text/csv')

        return {
            'statusCode': 200,
            'body': json.dumps({
                'Key': KEY,
                'Content': update_list
            })
        }
