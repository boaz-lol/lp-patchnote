import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()
db = mysql.connector.connect(
    host=os.environ.get("MYSQL_DB_URL"),
    user=os.environ.get("MYSQL_DB_USER"),
    passwd=os.environ.get("MYSQL_DB_PASSWORD"),
    database=os.environ.get("MYSQL_DB_NAME")
)

cur = db.cursor()
