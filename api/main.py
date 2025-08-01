from fastapi import FastAPI
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT")
)

@app.get("/")
def home():
    return {"message": "Dalilak API is working 🔥"}

@app.get("/test-db")
def test_db():
    cur = conn.cursor()
    cur.execute("SELECT name FROM guides LIMIT 3;")
    rows = cur.fetchall()
    return {"guides": rows}
