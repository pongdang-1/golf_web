from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import sqlite3
import json

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

class Coordinate(BaseModel):
    x: float
    y: float
    createdAt: Optional[str] = None


@app.get("/coordinates/{image}")
def get_coordinates(image: str):
    cursor.execute("SELECT data FROM coordinates WHERE image = ?", (image,))
    row = cursor.fetchone()
    if row:
        return json.loads(row[0])
    return []



@app.post("/coordinates/{image}")
def save_coordinates(image: str, coords: List[Coordinate]):
    # Pydantic 모델을 dict로 변환해서 저장
    data = json.dumps([c.model_dump() for c in coords], ensure_ascii=False)
    cursor.execute("INSERT OR REPLACE INTO coordinates (image, data) VALUES (?, ?)", (image, data))
    conn.commit()
    return {"status": "saved"}