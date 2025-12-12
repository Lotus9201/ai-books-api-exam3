from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel, Field

import database  

app = FastAPI(
    title="AI 書籍 API",
    description="這是一個提供書籍 CRUD 功能的 RESTful API 範例",
    version="1.0.0",
)


# ----------------------------
# Pydantic 模型
# ----------------------------

class BookCreate(BaseModel):
    title: str | None = None
    author: str | None = None
    publisher: str | None = None
    price: int = Field(..., gt=0, description="價格必須大於 0")
    publish_date: str | None = Field(None, description="出版日期 YYYY-MM-DD")
    isbn: str | None = None
    cover_url: str | None = None


class BookResponse(BookCreate):
    id: int
    created_at: str


# ----------------------------
# API 端點
# ----------------------------

@app.get("/", summary="首頁訊息", response_description="API 狀態訊息")
def root():
    return {"message": "歡迎使用 AI 書籍 API"}


@app.get("/books", summary="取得書籍列表", response_description="書籍資料列表")
def get_books(
    skip: int = Query(0, ge=0, description="從第幾筆開始"),
    limit: int = Query(10, ge=1, description="每頁顯示幾筆")
):
    books = database.get_all_books(skip, limit)
    return books


@app.get("/books/{book_id}", summary="取得單本書籍", response_description="單本書籍資料")
def get_book(
    book_id: int = Path(..., ge=1, description="書籍 ID")
):
    book = database.get_book_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="找不到書籍")
    return book


@app.post("/books", summary="新增書籍", response_description="新增後的書籍資料", status_code=201)
def create_book(book: BookCreate):
    book_id = database.create_book(
        book.title,
        book.author,
        book.publisher,
        book.price,
        book.publish_date,
        book.isbn,
        book.cover_url
    )
    new_book = database.get_book_by_id(book_id)
    return new_book


@app.put("/books/{book_id}", summary="更新書籍資料", response_description="更新後的書籍資料")
def update_book(
    book_id: int = Path(..., ge=1, description="書籍 ID"),
    book: BookCreate = ...
):
    exists = database.get_book_by_id(book_id)
    if not exists:
        raise HTTPException(status_code=404, detail="找不到書籍")

    updated = database.update_book(
        book_id,
        book.title,
        book.author,
        book.publisher,
        book.price,
        book.publish_date,
        book.isbn,
        book.cover_url
    )

    if not updated:
        raise HTTPException(status_code=404, detail="更新失敗")

    return database.get_book_by_id(book_id)


@app.delete("/books/{book_id}", summary="刪除書籍", status_code=204)
def delete_book(
    book_id: int = Path(..., ge=1, description="書籍 ID")
):
    deleted = database.delete_book(book_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="找不到書籍")
    return None
