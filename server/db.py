from sqlalchemy import create_engine, select, text
from dotenv import load_dotenv
import psycopg
import os

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

conn = psycopg.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASS,
    host=DB_HOST,
    port=DB_PORT
)

cur = conn.cursor()
cur.execute("SELECT now()")
print(cur.fetchone())
