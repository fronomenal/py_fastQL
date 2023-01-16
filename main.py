import os

import uvicorn
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware, db
from dotenv import load_dotenv

from models import Author
from models import Author as ModelAuthor
from models import Book
from models import Book as ModelBook
from schema import Author as SchemaAuthor
from schema import Book as SchemaBook

load_dotenv("./env_files/api.env")

app = FastAPI()

@app.get("/testing")
async def root():
    return {"message": os.getenv("TESTING")}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)