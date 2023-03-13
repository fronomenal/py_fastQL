import os

import uvicorn
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv

from db_conf import db_session
from models import Author
from models import Book
from schemas import Author as SchemaAuthor
from schemas import Book as SchemaBook


from starlette_graphene3 import GraphQLApp, make_graphiql_handler
from queries import schema

tags_metadata = [
    {
        "name": "books",
        "description": "Queries about books.",
    },
    {
        "name": "authors",
        "description": "Queries about authors of books.",
    },
]

db = db_session.session_factory()

app = FastAPI(openapi_tags=tags_metadata, title="Sloth's Books DB", description="Get rating info about books and their authors", version="0.1.0")

app.add_route("/graphql", GraphQLApp(schema, on_get=make_graphiql_handler()))

@app.get("/")
async def root():
    return {"message": "Welcome to the Fast Bookstore"}


@app.get("/books/", tags=["books"], response_model=list[SchemaBook])
def get_books() -> list[SchemaBook] :
    books = db.query(Book).all()
    return books

@app.get("/books/{id}", tags=["books"], response_model=SchemaBook)
def get_book(id: int):
    book = db.query(Book).filter(Book.id == id).first()
    if (book) : return book
    raise HTTPException(status_code=404, detail="Book not found")

@app.get("/authors/", tags=["authors"],  response_model=list[SchemaAuthor])
def get_authors() -> list[SchemaAuthor] :
    authors = db.query(Author).all()
    return authors

@app.get("/authors/{id}", tags=["authors"],  response_model=SchemaAuthor)
def get_author(id: int):
    author = db.query(Author).filter(Author.id == id).first()
    if (author) : return author
    raise HTTPException(status_code=404, detail="Author not found")

@app.post("/books/", tags=["books"], response_model=SchemaBook)
def add_book(book: SchemaBook):
    db_book = Book(title=book.title, rating=book.rating, author_id=book.author_id)
    try:
        db.add(db_book)
        db.commit()
        return db_book
    except:
        db.rollback()
    raise HTTPException(status_code=400, detail="Bad Request")
        

@app.post("/authors/", tags=["authors"],  response_model=SchemaAuthor)
def add_author(author: SchemaAuthor):
    db_author = Author(name=author.name, age=author.age)
    db.add(db_author)
    db.commit()
    return db_author

@app.delete("/books/{id}", tags=["books"], response_model=SchemaBook)
def delete_books(id: int):
    book = db.query(Book).filter(Book.id == id).first()
    if (book) : 
        db.delete(book)
        db.commit()
        return book
    raise HTTPException(status_code=404, detail="Book not found")

@app.delete("/authors/{id}", tags=["authors"],  response_model=SchemaAuthor)
def delete_authors(id: int):
    author = db.query(Author).filter(Author.id == id).first()
    if (author) : 
        db.delete(author)
        db.commit()
        return author
    raise HTTPException(status_code=404, detail="Author not found")



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)