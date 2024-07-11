# https://kr.api.riotgames.com/lol/league/v4/entries/RANKED_SOLO_5x5/IRON/I?page=10&api_key=RGAPI-91eeeae0-fb5b-4605-a818-96b93eef6994

import requests
import json

api_key="RGAPI-cac9b4e3-0b08-443f-a36a-61ada3e50505"

# 1. 유저 정보를 조회하는 api
# /riot/account/v1/accounts/by-riot-id/{유저 이름}/{유저 태그}
account = requests.get("https://asia.api.riotgames.com/riot/account/v1/accounts/by-riot-id/%EA%B1%B4%EC%95%BC%ED%98%B8/%EA%B3%A0%EC%96%91%EC%9D%B4?api_key={api_key}".format(api_key=api_key)).json()
print(requests.get("https://asia.api.riotgames.com/riot/account/v1/accounts/by-riot-id/%EA%B1%B4%EC%95%BC%ED%98%B8/%EA%B3%A0%EC%96%91%EC%9D%B4?api_key={api_key}".format(api_key=api_key)))
account_puid = account["puuid"]
print(account)

# 2. 최근 매치를 조건에 맞추서 가져오는 api(현재 20개
# /lol/match/v5/matches/by-puuid
match_id_list = requests.get(
    "https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/{user_puuid}/ids?start=0&count=40&api_key={api_key}"
    .format(user_puuid=account_puid, api_key=api_key)).json()
print(match_id_list)

# 3. 각 매치에 대한 정보를 조회하는 api
# /lol/match/v5/matches
match_info_url = "https://asia.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={api_key}"
for match in match_id_list:
    match_info = requests.get(match_info_url.format(match_id=match, api_key=api_key).json())

