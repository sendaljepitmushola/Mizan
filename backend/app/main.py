import os
import sqlite3
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

DB_FILE = "./database/sqlite/mizan.db"
if not os.path.exists(DB_FILE):
    DB_FILE = "mizan_hadith.db"

app = FastAPI(title="Mizan Hadith Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

def search_sqlite(query_str: str, limit: int = 20):
    results = []
    q_clean = query_str.strip().lower()

    if not q_clean or not os.path.exists(DB_FILE):
        return []

    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Cari hadis yang mengandung kata kunci pencarian
        # Mengutamakan hadis yang teks terjemahan Indonesianya valid dan mengandung kata kunci di posisi awal/penting
        sql = """
            SELECT 
                h.id, 
                COALESCE(b.title_en, b.title_ar, 'Kitab Hadis') AS book_name, 
                h.hadith_number, 
                h.arabic, 
                h.translation_id, 
                h.translation_en
            FROM hadiths h
            LEFT JOIN books b ON h.book_id = b.id
            WHERE LOWER(h.translation_id) LIKE ? 
               OR LOWER(h.arabic) LIKE ?
            ORDER BY 
                CASE 
                    WHEN LOWER(h.translation_id) LIKE ? THEN 1
                    ELSE 2 
                END,
                CAST(h.hadith_number AS INTEGER) ASC
            LIMIT ?
        """
        exact_pattern = f"% {q_clean} %"
        like_pattern = f"%{q_clean}%"
        
        cursor.execute(sql, (like_pattern, like_pattern, exact_pattern, limit))
        rows = cursor.fetchall()
        conn.close()

        for r in rows:
            results.append({
                "id": str(r[0]),
                "hadith_id": str(r[0]),
                "book_id": r[1],
                "book_name": r[1],
                "hadith_number": str(r[2]),
                "arabic": r[3] or "",
                "translation": r[4] or r[5] or "",
                "translation_id": r[4] or "",
                "translation_en": r[5] or "",
                "source": "SQLite Direct"
            })
    except Exception as e:
        print(f"SQL Search Error: {e}")

    return results

@app.options("/{full_path:path}")
async def options_handler(full_path: str):
    return JSONResponse(content={"status": "ok"})

@app.get("/api/v1/search")
@app.get("/search")
@app.get("/hadiths/search")
@app.get("/api/hadiths/search")
async def api_search(request: Request):
    q = request.query_params.get("q") or request.query_params.get("query") or ""
    data = search_sqlite(q)
    return JSONResponse(content={
        "status": "success",
        "query": q,
        "total": len(data),
        "results": data,
        "data": data,
        "hadiths": data
    })

@app.get("/api/v1/books")
@app.get("/books")
def get_books():
    if not os.path.exists(DB_FILE):
        return {"status": "success", "data": []}
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT id, slug, title_en, title_ar, total_hadith FROM books")
        rows = cursor.fetchall()
        conn.close()
        
        books = [{
            "id": r[0],
            "slug": r[1],
            "name": r[2] or r[3],
            "title_en": r[2],
            "title_ar": r[3],
            "total_hadith": r[4] if len(r) > 4 else 0
        } for r in rows]
        return {"status": "success", "data": books, "books": books}
    except Exception as e:
        return {"status": "error", "message": str(e), "data": []}

if os.path.exists("frontend"):
    app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend_assets")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
