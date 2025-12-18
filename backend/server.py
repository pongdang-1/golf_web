from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import json
from typing import List, Dict

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 데이터베이스 초기화
conn = sqlite3.connect('coordinates.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS coordinates (
        image TEXT PRIMARY KEY,
        data TEXT
    )
''')
conn.commit()

@app.get("/coordinates/{image}")
def get_coordinates(image: str):
    cursor.execute("SELECT data FROM coordinates WHERE image = ?", (image,))
    row = cursor.fetchone()
    if row:
        return json.loads(row[0])
    return []



@app.post("/coordinates/{image}")
def save_coordinates(image: str, coords: List[Dict[str, float]]):
    data = json.dumps(coords)
    cursor.execute("INSERT OR REPLACE INTO coordinates (image, data) VALUES (?, ?)", (image, data))
    conn.commit()
    return {"status": "saved"}