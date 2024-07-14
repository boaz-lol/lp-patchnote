import sys
import os

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from pymongo import MongoClient
import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.preprocessing import StandardScaler

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import get_db
from app.schemas.query import QueryModel

router = APIRouter()
db = get_db()

@router.post("/predict")
def predict(query: QueryModel):
    query_dict = {"puuid": query.puuid}
    
    data_source_collection = db["data_source"]
    data = list(data_source_collection.find(query_dict))
    if not data:
        raise HTTPException(status_code=404, detail="Data not found for the given PUUID")
    
    df = pd.DataFrame(data)
    
    mlflow.set_tracking_uri(uri="http://13.209.9.231:5000")
    model_uri = "models:/extra-test-0620/4"  
    loaded_model = mlflow.sklearn.load_model(model_uri)
    
    X = df.drop(['_id', 'win', 'match_id', "puuid", "query_game_name", "created_at", 'championId', 'role'], axis=1)
    scaler = StandardScaler()
    X = scaler.fit_transform(X)
    
    predictions = loaded_model.predict_proba(X)
    
    return JSONResponse(content={"predictions": predictions.tolist()[0][1]})