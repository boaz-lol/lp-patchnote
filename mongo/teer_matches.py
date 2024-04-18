# https://kr.api.riotgames.com/lol/league/v4/entries/RANKED_SOLO_5x5/IRON/I?page=10&api_key=RGAPI-91eeeae0-fb5b-4605-a818-96b93eef6994

import requests
import json

api_key=""
account = requests.get("https://asia.api.riotgames.com/riot/account/v1/accounts/by-riot-id/%EA%B1%B4%EC%95%BC%ED%98%B8/%EA%B3%A0%EC%96%91%EC%9D%B4?api_key={api_key}".format(api_key=api_key)).json()
account_puid = account["puuid"]
print(account)

match_id_list = requests.get(
    "https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/{user_puuid}/ids?start=0&count=20&api_key={api_key}"
    .format(user_puuid=account_puid, api_key=api_key)).json()
print(match_id_list)

match_info_url = "https://asia.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={api_key}"
for match in match_id_list:
    print(requests.get(match_info_url.format(match_id=match, api_key=api_key)).json())
