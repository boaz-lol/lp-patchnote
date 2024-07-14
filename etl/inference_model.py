import os
import pandas as pd
import requests
from datetime import datetime, timedelta

import mlflow
from pymongo import MongoClient
from dotenv import load_dotenv
from sklearn.preprocessing import StandardScaler, LabelEncoder


if __name__ == '__main__':
    uri = os.getenv("MONGO_URI")
    client = MongoClient(uri)

    db = client["lpdb"]
    ml_inference_collection = db["ml_inference"]
    data_source_collection = db["data_source"]

    start_date = datetime(2024, 7, 11)
    end_date = start_date + timedelta(days=1)

    # 쿼리 실행
    query = {
        "puuid": '5YEyzGrRYekE-otAW8-K8vrzzMezrRg1Dy_8MFModSadlnf-jkZv9I8KgLD34_Bxf_A7PwGSxNflDQ' ,
    }

    # 결과 가져오기
    data = list(data_source_collection.find(query))

    df = pd.DataFrame(data)

    mlflow.set_tracking_uri(uri="http://13.209.9.231:5000")
    model_uri = "models:/extra-test-0620/4"  # 버전 번호에 따라 수정 필요
    loaded_model = mlflow.sklearn.load_model(model_uri)

    X = df.drop(['_id','win', 'match_id',"puuid","query_game_name","created_at",'championId','championId','role'], axis=1)  
    encoder = LabelEncoder()
    # X["role"] = encoder.fit_transform(X['role'])
    scaler = StandardScaler() 
    X = scaler.fit_transform(X)
    predictions = loaded_model.predict_proba(X)

    teer_list = list(map(lambda proba: proba[1], predictions))
    indexed_teer_list = list(enumerate(teer_list))
    sorted_indexed_teer_list = sorted(
        indexed_teer_list, key = lambda x: x[1], reverse=True
    )

    print(f"{data[0]['query_game_name']} 유저의 7.11 ~ 7.12 ")
    for idx, teer in enumerate(sorted_indexed_teer_list):
        champion_id = data[idx]["championId"]
        print(f"Champion Id: {champion_id} LP Teer: {teer[1]*100:.1f}/100 점")