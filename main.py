import os

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi_sqlalchemy import DBSessionMiddleware, db
from dotenv import load_dotenv

from models import Author
from models import Book
from schema import Author as SchemaAuthor
from schema import Book as SchemaBook

load_dotenv("./env_files/api.env")

app = FastAPI(title="Sloth's Books DB", description="Get rating info about books and their authors", version="0.1.0")

app.add_middleware(DBSessionMiddleware, db_url=os.getenv("DATABASE_URL"))

@app.get("/")
async def root():
    return {"message": "Welcome to the Fast Bookstore"}


@app.get("/books/", response_model=list[SchemaBook])
def get_books() -> list[SchemaBook] :
    books = db.session.query(Book).all()
    return books

@app.get("/books/{id}", response_model=SchemaBook)
def get_books(id: int):
    book = db.session.query(Book).filter(Book.id == id).first()
    if (book) : return book
    raise HTTPException(status_code=404, detail="Book not found")

@app.get("/authors/", response_model=list[SchemaAuthor])
def get_authors() -> list[SchemaAuthor] :
    authors = db.session.query(Author).all()
    return authors

@app.get("/authors/{id}", response_model=SchemaAuthor)
def get_authors(id: int):
    author = db.session.query(Author).filter(Author.id == id).first()
    if (author) : return author
    raise HTTPException(status_code=404, detail="Author not found")

@app.post("/books/", response_model=SchemaBook)
def add_book(book: SchemaBook):
    db_book = Book(title=book.title, rating=book.rating, author_id=book.author_id)
    db.session.add(db_book)
    db.session.commit()
    return db_book


@app.post("/authors/", response_model=SchemaAuthor)
def add_author(author: SchemaAuthor):
    db_author = Author(name=author.name, age=author.age)
    db.session.add(db_author)
    db.session.commit()
    return db_author



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)