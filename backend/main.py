from fastapi import FastAPI, HTTPException
from models import Meme, MemeCreate
from typing import List, Optional
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Meme Gallery API", version="1.0")

# Тестова база даних у пам'яті
memes_db: List[Meme] = []
next_id = 1

# CORS (якщо треба фронту)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# GET: Отримати всі меми
@app.get("/memes", response_model=List[Meme])
def get_memes(category: Optional[str] = None, sort: Optional[str] = "newest"):
    memes = memes_db
    if category:
        memes = [m for m in memes if m.category == category]
    if sort == "newest":
        memes.sort(key=lambda m: m.created_at, reverse=True)
    return memes

# GET: Отримати мем за ID
@app.get("/memes/{meme_id}", response_model=Meme)
def get_meme(meme_id: int):
    for meme in memes_db:
        if meme.id == meme_id:
            return meme
    raise HTTPException(status_code=404, detail="Meme not found")

# GET: Список категорій
@app.get("/categories", response_model=List[str])
def get_categories():
    return list(set(m.category for m in memes_db))

# POST: Додати новий мем
@app.post("/memes", response_model=Meme, status_code=201)
def create_meme(meme: MemeCreate):
    global next_id
    new_meme = Meme(id=next_id, created_at=datetime.utcnow(), **meme.dict())
    memes_db.append(new_meme)
    next_id += 1
    return new_meme

# DELETE: Видалити мем за ID
@app.delete("/memes/{meme_id}", status_code=204)
def delete_meme(meme_id: int):
    for i, meme in enumerate(memes_db):
        if meme.id == meme_id:
            del memes_db[i]
            return
    raise HTTPException(status_code=404, detail="Meme not found")
