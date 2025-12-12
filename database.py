import sqlite3

# 建立資料庫連線
def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect("bokelai.db")
    conn.row_factory = sqlite3.Row  # 讓查詢結果可以像 dict
    return conn


# 取得所有書籍（支援 skip, limit）
def get_all_books(skip: int, limit: int) -> list[dict]:
    conn = get_db_connection()
    cursor = conn.execute(
        "SELECT * FROM books LIMIT ? OFFSET ?",
        (limit, skip)
    )
    books = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return books


# 依 ID 取得單一本書
def get_book_by_id(book_id: int) -> dict | None:
    conn = get_db_connection()
    cursor = conn.execute(
        "SELECT * FROM books WHERE id = ?",
        (book_id,)
    )
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


# 新增書籍，回傳新書的 id
def create_book(
    title: str,
    author: str,
    publisher: str | None,
    price: int,
    publish_date: str | None,
    isbn: str | None,
    cover_url: str | None
) -> int:
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


# 更新書籍資料，回傳是否成功
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


# 刪除書籍
def delete_book(book_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.execute(
        "DELETE FROM books WHERE id = ?",
        (book_id,)
    )
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    return deleted
