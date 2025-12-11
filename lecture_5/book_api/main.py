from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import Response
import models
import database
import schemas
import uvicorn

app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Добро пожаловать в Book API!"}

@app.get("/favicon.ico")
async def favicon():
    return Response(status_code=204)

# POST /books/
@app.post("/books/", response_model=schemas.BookOut)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

# GET /books/
@app.get("/books/", response_model=list[schemas.BookOut])
def read_books(db: Session = Depends(get_db)):
    return db.query(models.Book).all()

# DELETE /books/{book_id}
@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return {"message": "Book deleted successfully"}

# PUT /books/{book_id}
@app.put("/books/{book_id}", response_model=schemas.BookOut)
def update_book(book_id: int, updated_book: schemas.BookUpdate, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    for key, value in updated_book.dict(exclude_unset=True).items():
        setattr(book, key, value)
    db.commit()
    db.refresh(book)
    return book

# GET /books/search/
@app.get("/books/search/", response_model=list[schemas.BookOut])
def search_books(title: str = None, author: str = None, year: int = None, db: Session = Depends(get_db)):
    query = db.query(models.Book)
    if title:
        query = query.filter(models.Book.title.contains(title))
    if author:
        query = query.filter(models.Book.author.contains(author))
    if year:
        query = query.filter(models.Book.year == year)
    return query.all()

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
