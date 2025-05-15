from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

from models import Meme, MemeCreate, MemeDB
from database import SessionLocal, engine, Base

app = FastAPI(title="Meme API with DB")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # або ["http://localhost:8080"] для безпеки
    allow_credentials=True,
    allow_methods=["*"],  # ← ОБОВʼЯЗКОВО! дозволяє POST, OPTIONS тощо
    allow_headers=["*"],  # ← ОБОВʼЯЗКОВО! дозволяє заголовки, напр. Content-Type
)

# Створення таблиць
Base.metadata.create_all(bind=engine)

# Залежність для отримання сесії
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# GET: Отримати всі меми
@app.get("/memes", response_model=List[Meme])
def get_memes(category: Optional[str] = None, sort: Optional[str] = "newest", db: Session = Depends(get_db)):
    query = db.query(MemeDB)
    if category:
        query = query.filter(MemeDB.category == category)
    if sort == "newest":
        query = query.order_by(MemeDB.created_at.desc())
    return query.all()

# GET: Мем за ID
@app.get("/memes/{meme_id}", response_model=Meme)
def get_meme(meme_id: int, db: Session = Depends(get_db)):
    meme = db.query(MemeDB).filter(MemeDB.id == meme_id).first()
    if not meme:
        raise HTTPException(status_code=404, detail="Meme not found")
    return meme

# GET: Категорії
@app.get("/categories", response_model=List[str])
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(MemeDB.category).distinct().all()
    return [c[0] for c in categories]

# POST: Додати новий мем
@app.post("/memes", response_model=Meme, status_code=201)
def create_meme(meme: MemeCreate, db: Session = Depends(get_db)):
    new_meme = MemeDB(**meme.dict(), created_at=datetime.utcnow())
    db.add(new_meme)
    db.commit()
    db.refresh(new_meme)
    return new_meme

# DELETE: Видалити мем
@app.delete("/memes/{meme_id}", status_code=204)
def delete_meme(meme_id: int, db: Session = Depends(get_db)):
    meme = db.query(MemeDB).filter(MemeDB.id == meme_id).first()
    if not meme:
        raise HTTPException(status_code=404, detail="Meme not found")
    db.delete(meme)
    db.commit()
