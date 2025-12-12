
from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel, Field
import database  # 連接你的 database.py

app = FastAPI(
    title="AI 書籍 API",
    description="這是一個提供書籍 CRUD 功能的 RESTful API 範例",
    version="1.0.0",
)


# ----------------------------
# Pydantic Models
# ----------------------------

class BookCreate(BaseModel):
    """
    BookCreate 模型
    用於新增與更新書籍時的資料驗證。

    屬性:
        title (str | None): 書名
        author (str | None): 作者
        publisher (str | None): 出版社
        price (int): 價格（必須大於 0)
        publish_date (str | None): 出版日期
        isbn (str | None): ISBN 編號
        cover_url (str | None): 書籍封面圖片 URL
    """
    title: str | None = None
    author: str | None = None
    publisher: str | None = None
    price: int = Field(..., gt=0, description="價格必須大於 0")
    publish_date: str | None = None
    isbn: str | None = None
    cover_url: str | None = None


class BookResponse(BookCreate):
    """
    BookResponse 模型
    回傳書籍資訊時使用，包含資料庫自動產生的欄位。

    屬性:
        id (int): 書籍 ID
        created_at (str): 建立時間（ISO 格式字串）
    """
    id: int
    created_at: str


# ----------------------------
# API Routes
# ----------------------------

@app.get("/", summary="首頁訊息", response_description="API 狀態訊息")
def root():
    """
    API 首頁。

    回傳:
        dict: API 狀態資訊。
    """
    return {"message": "歡迎使用 AI 書籍 API"}


@app.get("/books", summary="取得書籍列表", response_description="書籍資料列表")
def get_books(
    skip: int = Query(0, ge=0, description="從第幾筆開始"),
    limit: int = Query(10, ge=1, description="每頁顯示幾筆")
):
    """
    取得書籍列表（分頁）。

    參數:
        skip (int): 跳過筆數
        limit (int): 取得筆數

    回傳:
        list[dict]: 書籍資料列表
    """
    books = database.get_all_books(skip, limit)
    return books


@app.get("/books/{book_id}", summary="取得單本書籍", response_description="單本書籍資料")
def get_book(
    book_id: int = Path(..., ge=1, description="書籍 ID")
):
    """
    依 ID 取得單一本書籍。

    參數:
        book_id (int): 書籍 ID

    回傳:
        dict: 書籍資訊

    例外:
        404: 找不到書籍
    """
    book = database.get_book_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="找不到書籍")
    return book


@app.post("/books", summary="新增書籍", response_description="新增後的書籍資料", status_code=201)
def create_book(book: BookCreate):
    """
    新增書籍資料。

    參數:
        book (BookCreate): 新書資料

    回傳:
        dict: 新增後的書籍完整資料
    """
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
    """
    更新書籍資料。

    參數:
        book_id (int): 書籍 ID
        book (BookCreate): 書籍新資料

    回傳:
        dict: 更新後的書籍資訊

    例外:
        404: 書籍不存在或更新失敗
    """
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
    """
    刪除書籍。

    參數:
        book_id (int): 書籍 ID

    回傳:
        None

    例外:
        404: 書籍不存在
    """
    deleted = database.delete_book(book_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="找不到書籍")
    return None
