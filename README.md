1.**如何啟動 FastAPI 伺服器**  
指令:uvicorn app:app --reload  

2.**啟動後能使用:**
Swagger UI（測API）  
http://127.0.0.1:8000/docs

ReDoc（文件瀏覽）  
http://127.0.0.1:8000/redoc

3.**API**  
(一)取得全部書籍    
    GET /books

(二)新增書籍  
    範例:{"title":"測試書","author":"我","price":999}
    
(三)查詢單本書籍  
    GET /books/{book_id}

(四)更新書籍  
    PUT /books/{book_id}

(五)刪除書籍  
    DELETE /books/{book_id}
 

