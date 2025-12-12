from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field

class BookCreate(BaseModel):
    title: str = Field(..., min_length=1)
    author: str = Field(..., min_length=1)
    publisher: str | None = None
    price: int = Field(..., gt=0)
    publish_date: str | None = None
    isbn: str | None = None
    cover_url: str | None = None

    model_config = ConfigDict(
        anystr_strip_whitespace=True
    )


class BookResponse(BookCreate):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
