from pydantic import BaseModel, Field


class Book(BaseModel):
    id: str = Field(description="Unique identifier of the book")
    title: str = Field(description="Book title")
    author: str = Field(description="Book author")
    year: int = Field(description="Publication year")
