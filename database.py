import sqlite3


def get_db_connection() -> sqlite3.Connection:
    """
    SQLite 資料庫連線。

    回傳:
        sqlite3.Connection: 資料庫連線物件
    """
    conn = sqlite3.connect("bokelai.db")
    conn.row_factory = sqlite3.Row  # 查詢結果轉成 dict-like 結構
    return conn


def get_all_books(skip: int, limit: int) -> list[dict]:
    """
    取得所有書籍（支援分頁）。

    參數:
        skip (int): 跳過筆數
        limit (int): 取得筆數

    回傳:
        list[dict]: 書籍資料列表
    """
    conn = get_db_connection()
    cursor = conn.execute(
        "SELECT * FROM books LIMIT ? OFFSET ?",
        (limit, skip)
    )
    books = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return books


def get_book_by_id(book_id: int) -> dict | None:
    """
    依照ID來取得單一本書籍。

    參數:
        book_id (int): 書籍 ID

    回傳:
        dict | None: 書籍資料，找不到則回傳 None
    """
    conn = get_db_connection()
    cursor = conn.execute(
        "SELECT * FROM books WHERE id = ?",
        (book_id,)
    )
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def create_book(
    title: str,
    author: str,
    publisher: str | None,
    price: int,
    publish_date: str | None,
    isbn: str | None,
    cover_url: str | None
) -> int:
    """
    新增書籍。

    參數:
        title (str): 書名
        author (str): 作者
        publisher (str | None): 出版社
        price (int): 價格
        publish_date (str | None): 出版日期
        isbn (str | None): ISBN 編號
        cover_url (str | None): 封面 URL

    回傳:
        int: 新增書籍的 ID
    """
    conn = get_db_connection()
    cursor = conn.execute(
        """
        INSERT INTO books (title, author, publisher, price, publish_date, isbn, cover_url)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (title, author, publisher, price, publish_date, isbn, cover_url)
    )
    conn.commit()
    book_id = cursor.lastrowid
    conn.close()
    return book_id


def update_book(
    book_id: int,
    title: str,
    author: str,
    publisher: str | None,
    price: int,
    publish_date: str | None,
    isbn: str | None,
    cover_url: str | None
) -> bool:
    """
    更新書籍資料。

    參數:
        book_id (int): 書籍 ID
        title (str): 書名
        author (str): 作者
        publisher (str | None): 出版社
        price (int): 價格
        publish_date (str | None): 出版日期
        isbn (str | None): ISBN
        cover_url (str | None): 封面 URL

    回傳:
        bool: 是否成功更新
    """
    conn = get_db_connection()
    cursor = conn.execute(
        """
        UPDATE books
        SET title = ?, author = ?, publisher = ?, price = ?, publish_date = ?, isbn = ?, cover_url = ?
        WHERE id = ?
        """,
        (title, author, publisher, price, publish_date, isbn, cover_url, book_id)
    )
    conn.commit()
    updated = cursor.rowcount > 0
    conn.close()
    return updated


def delete_book(book_id: int) -> bool:
    """
    刪除書籍。

    參數:
        book_id (int): 書籍 ID

    回傳:
        bool: 是否成功刪除
    """
    conn = get_db_connection()
    cursor = conn.execute(
        "DELETE FROM books WHERE id = ?",
        (book_id,)
    )
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    return deleted
