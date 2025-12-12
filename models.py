from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class BookCreate(BaseModel):
    """
    新增與更新書籍時的資料驗證。

    屬性:
        title (str): 書名
        author (str): 作者
        publisher (str | None): 出版社
        price (int): 價格（必須大於 0）
        publish_date (str | None): 出版日期
        isbn (str | None): ISBN 編號
        cover_url (str | None): 書籍封面 URL
    """

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
    """
    BookResponse 模型
    用於 API 回傳與序列化使用。

    屬性:
        id (int): 書籍 ID
        created_at (datetime): 建立時間
    """

    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
