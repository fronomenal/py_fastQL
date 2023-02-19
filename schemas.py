from pydantic import BaseModel, Field
from graphene_sqlalchemy import SQLAlchemyObjectType

from models import Post


class Book(BaseModel):
    """Book Item"""
    
    title: str = Field(description="Title of the book")
    rating: int = Field(description="Rating of the Book")
    author_id: int = Field(description="ID of book author")

    class Config:
        orm_mode = True

class Author(BaseModel):
    """Book Author"""
    
    name: str = Field(description="Name of Author")
    age: int = Field(description="Age of Author")

    class Config:
        orm_mode = True


class PostSchema(BaseModel):
    title: str
    content: str

class PostModel(SQLAlchemyObjectType):
    class Meta:
        model = Post

class UserSchema(BaseModel):
    username: str
    password: str