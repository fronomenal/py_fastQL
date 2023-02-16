from pydantic import BaseModel, Field


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
