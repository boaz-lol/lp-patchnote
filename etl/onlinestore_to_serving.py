from datetime import datetime, timedelta

import mlflow
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder


if __name__ == '__main__':

    # Make Fake Input Data
    # Condition 1) Different 10 Champions.
    # Condition 2) Recent 10 matches.

    data = [
        {'query_game_name':"건야호",'query_date':'2024-06-20','match_id': 'KR_7064313798', 'puuid': '11_54_34', 'role': 'DUO', 'championId': 123, 'champLevel': 12, 'win': False, 'damages_per_minute': 1080.567, 'damageTakenOnTeamPercentage': 0.178, 'goldPerMinute': 644.1, 'teamDamagePercentage': 0.171, 'kda': 2.39},
        {'query_game_name':"건야호",'query_date':'2024-06-20','match_id': 'KR_7064313799', 'puuid': '42_11_93', 'role': 'SOLO', 'championId': 89, 'champLevel': 16, 'win': True, 'damages_per_minute': 1274.321, 'damageTakenOnTeamPercentage': 0.193, 'goldPerMinute': 678.9, 'teamDamagePercentage': 0.202, 'kda': 3.12},
        {'query_game_name':"건야호",'query_date':'2024-06-20','match_id': 'KR_7064313800', 'puuid': '19_64_12', 'role': 'JUNGLE', 'championId': 45, 'champLevel': 15, 'win': False, 'damages_per_minute': 950.643, 'damageTakenOnTeamPercentage': 0.165, 'goldPerMinute': 523.5, 'teamDamagePercentage': 0.143, 'kda': 1.88},
        {'query_game_name':"건야호",'query_date':'2024-06-20','match_id': 'KR_7064313801', 'puuid': '33_23_87', 'role': 'SUPPORT', 'championId': 77, 'champLevel': 10, 'win': True, 'damages_per_minute': 620.789, 'damageTakenOnTeamPercentage': 0.156, 'goldPerMinute': 389.2, 'teamDamagePercentage': 0.132, 'kda': 2.75},
        {'query_game_name':"건야호",'query_date':'2024-06-20','match_id': 'KR_7064313802', 'puuid': '21_75_30', 'role': 'MID', 'championId': 102, 'champLevel': 14, 'win': True, 'damages_per_minute': 1345.982, 'damageTakenOnTeamPercentage': 0.204, 'goldPerMinute': 755.4, 'teamDamagePercentage': 0.213, 'kda': 4.01},
        {'query_game_name':"건야호",'query_date':'2024-06-20','match_id': 'KR_7064313803', 'puuid': '54_82_47', 'role': 'DUO', 'championId': 99, 'champLevel': 13, 'win': False, 'damages_per_minute': 889.345, 'damageTakenOnTeamPercentage': 0.132, 'goldPerMinute': 601.5, 'teamDamagePercentage': 0.156, 'kda': 2.22},
        {'query_game_name':"건야호",'query_date':'2024-06-20','match_id': 'KR_7064313804', 'puuid': '12_38_90', 'role': 'SOLO', 'championId': 68, 'champLevel': 18, 'win': True, 'damages_per_minute': 1456.721, 'damageTakenOnTeamPercentage': 0.213, 'goldPerMinute': 712.3, 'teamDamagePercentage': 0.234, 'kda': 4.55},
        {'query_game_name':"건야호",'query_date':'2024-06-20','match_id': 'KR_7064313805', 'puuid': '25_60_21', 'role': 'JUNGLE', 'championId': 58, 'champLevel': 17, 'win': False, 'damages_per_minute': 1189.654, 'damageTakenOnTeamPercentage': 0.191, 'goldPerMinute': 632.8, 'teamDamagePercentage': 0.198, 'kda': 3.18},
        {'query_game_name':"건야호",'query_date':'2024-06-20','match_id': 'KR_7064313806', 'puuid': '17_51_73', 'role': 'SUPPORT', 'championId': 36, 'champLevel': 11, 'win': True, 'damages_per_minute': 715.987, 'damageTakenOnTeamPercentage': 0.144, 'goldPerMinute': 477.9, 'teamDamagePercentage': 0.154, 'kda': 2.95},
        {'query_game_name':"건야호",'query_date':'2024-06-20','match_id': 'KR_7064313807', 'puuid': '90_12_45', 'role': 'MID', 'championId': 110, 'champLevel': 9, 'win': False, 'damages_per_minute': 805.654, 'damageTakenOnTeamPercentage': 0.174, 'goldPerMinute': 538.4, 'teamDamagePercentage': 0.167, 'kda': 2.11}
    ]
    df = pd.DataFrame(data)

    # Load Model from MLFlow
    mlflow.set_tracking_uri(uri="http://13.209.9.231:5000")
    model_uri = "models:/extra-test-0620/1"  # 버전 번호에 따라 수정 필요
    loaded_model = mlflow.sklearn.load_model(model_uri)

    # Make Inference
    X = df.drop(['win', 'match_id',"puuid","query_game_name","query_date"], axis=1)  
    encoder = LabelEncoder()
    X["role"] = encoder.fit_transform(X['role'])
    scaler = StandardScaler() 
    X = scaler.fit_transform(X)
    predictions = loaded_model.predict_proba(X)

    teer_list = list(map(lambda proba: proba[1], predictions))
    indexed_teer_list = list(enumerate(teer_list))
    sorted_indexed_teer_list = sorted(
        indexed_teer_list, key = lambda x: x[1], reverse=True
    )
    print(f"{data[0]['query_game_name']} 유저의 최근 플레이한 10명 챔피언의 LP Teer")
    for idx, teer in enumerate(sorted_indexed_teer_list):
        champion_id = data[idx]["championId"]
        print(f"Champion Id: {champion_id} LP Teer: {teer[1]*100:.1f}/100 점")

