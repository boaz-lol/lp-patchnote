import os
from datetime import datetime, timedelta

from pymongo import MongoClient
from dotenv import load_dotenv
import pandas as pd
import pyarrow.parquet as pq
import pyarrow as pa
from io import BytesIO
import boto3

if __name__ == '__main__':
    uri = os.getenv("MONGO_URI")
    client = MongoClient(uri)

    db = client["lpdb"]
    collection = db["data_source"]

    ## extract documents from MongoDB a
    today = datetime.now().date()
    start_date = datetime(today.year, today.month, today.day)
    end_date = start_date + timedelta(days=1)

    query_game_name = "건야호"

    query = {
        "query_game_name": query_game_name,
        "query_date": {
            "$gte": start_date,
            "$lt": end_date
        }
    }
    documents = list(collection.find(query))
    for document in documents:
        print(document)

    ## write parquet on S3
    filtered_documents = [{key: value for key, value in document.items() if key != '_id'} for document in documents]
    df = pd.DataFrame(filtered_documents)
    table = pa.Table.from_pandas(df)
    buffer = BytesIO()
    pq.write_table(table, buffer)
    buffer.seek(0)

    s3_client = boto3.client('s3')
    bucket_name = 'boazengineerlp'
    file_path = f'offline-store/{query_game_name}_{start_date}.parquet'
    s3_client.upload_fileobj(buffer, bucket_name, file_path)
    print(f"File uploaded to S3 at s3://{bucket_name}/{file_path}")