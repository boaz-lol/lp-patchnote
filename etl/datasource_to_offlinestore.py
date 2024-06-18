import json
import os
import requests
from datetime import datetime, timedelta

from pymongo import MongoClient
from dotenv import load_dotenv

if __name__ == '__main__':
    uri = os.getenv("MONGO_URI")
    client = MongoClient(uri)

    db = client["lpdb"]
    collection = db["data_source"]

    # get json list
    api_key = os.getenv("RIOT_API_KEY")
    account = requests.get("https://asia.api.riotgames.com/riot/account/v1/accounts/by-riot-id/%EA%B1%B4%EC%95%BC%ED%98%B8/%EA%B3%A0%EC%96%91%EC%9D%B4?api_key={api_key}".format(api_key=api_key)).json()
    account_puid = account["puuid"]
    print(account)
    match_id_list = requests.get(
        "https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/{user_puuid}/ids?start=0&count=10&api_key={api_key}"
        .format(user_puuid=account_puid, api_key=api_key)
    ).json()

    # insert to MongoDB
    match_info_url = "https://asia.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={api_key}"
    row_list = []
    for match in match_id_list:
        match_data = requests.get(match_info_url.format(match_id=match, api_key=api_key)).json()
        match_participants = match_data["info"]["participants"]
        for participant_num in range(len(match_participants)):
            # GET 날린 user puuid, 날짜 추가"
            participant_match_data = { "query_game_name": account["gameName"] }
            participant_match_data["query_date"] = datetime.now()
            participant_match_data["match_id"] = match
            participant_match_data["puuid"] = match_data["info"]["participants"][participant_num]["puuid"]
            participant_match_data["role"] = match_data["info"]["participants"][participant_num]["role"]
            participant_match_data["championId"] = match_data["info"]["participants"][participant_num]["championId"]
            participant_match_data["champLevel"] = match_data["info"]["participants"][participant_num]["champLevel"]
            participant_match_data["win"] = match_data["info"]["participants"][participant_num]["win"]

            # challenges
            participant_match_data["damages_per_minute"] = match_data["info"]["participants"][participant_num]["challenges"]["damagePerMinute"]
            participant_match_data["damageTakenOnTeamPercentage"] = match_data["info"]["participants"][participant_num]["challenges"]["damageTakenOnTeamPercentage"]
            participant_match_data["goldPerMinute"] = match_data["info"]["participants"][participant_num]["challenges"]["goldPerMinute"]
            participant_match_data["teamDamagePercentage"] = match_data["info"]["participants"][participant_num]["challenges"]["teamDamagePercentage"]
            participant_match_data["kda"] = match_data["info"]["participants"][participant_num]["challenges"]["kda"]

            inserted_id = collection.insert_one(participant_match_data).inserted_id
            print(f"Document inserted with _id: {inserted_id}")

    # extract documents from MongoDB and write parquet on S3

    today = datetime.now().date()
    start_date = datetime(today.year, today.month, today.day)
    end_date = start_date + timedelta(days=1)

    query = {
        "query_game_name": "건야호",
        "query_date": {
            "$gte": start_date,
            "$lt": end_date
        }
    }
    documents = collection.find(query)
    for document in documents:
        print(document)

    