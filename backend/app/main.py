from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .database import SessionLocal
from .models import Book, Hadith
from .schemas import BookResponse, HadithResponse
from .search import search_hadith

app = FastAPI(
    title="Project Mizan API",
    description="API untuk pencarian, verifikasi, dan eksplorasi hadis.",
    version="0.1.0",
)

# Izinkan request dari frontend (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "Welcome to Project Mizan API",
        "project": "Project Mizan",
        "version": "0.1.0",
        "status": "development",
    }


@app.get("/books", response_model=list[BookResponse])
def get_books():
    session = SessionLocal()
    books = session.query(Book).order_by(Book.id).all()
    session.close()
    return books


@app.get("/books/{slug}", response_model=BookResponse)
def get_book(slug: str):
    session = SessionLocal()

    book = session.query(Book).filter(Book.slug == slug).first()

    if book is None:
        session.close()
        raise HTTPException(status_code=404, detail="Book not found")

    session.close()
    return book


@app.get("/books/{slug}/hadiths", response_model=list[HadithResponse])
def get_book_hadiths(slug: str, skip: int = 0, limit: int = 100):
    session = SessionLocal()

    book = session.query(Book).filter(Book.slug == slug).first()

    if book is None:
        session.close()
        raise HTTPException(status_code=404, detail="Book not found")

    hadiths = (
        session.query(Hadith)
        .filter(Hadith.book_id == book.id)
        .order_by(Hadith.hadith_number)
        .offset(skip)
        .limit(limit)
        .all()
    )

    session.close()
    return hadiths


@app.get("/books/{slug}/hadiths/{hadith_number}", response_model=HadithResponse)
def get_book_hadith(slug: str, hadith_number: int):
    session = SessionLocal()

    book = session.query(Book).filter(Book.slug == slug).first()

    if book is None:
        session.close()
        raise HTTPException(status_code=404, detail="Book not found")

    hadith = (
        session.query(Hadith)
        .filter(
            Hadith.book_id == book.id,
            Hadith.hadith_number == hadith_number,
        )
        .first()
    )

    if hadith is None:
        session.close()
        raise HTTPException(status_code=404, detail="Hadith not found")

    session.close()
    return hadith


@app.get("/hadiths/search", response_model=list[HadithResponse])
def search(q: str):
    session = SessionLocal()

    result = search_hadith(session, q)

    session.close()
    return result


@app.get("/hadiths", response_model=list[HadithResponse])
def get_hadiths(skip: int = 0, limit: int = 100):
    session = SessionLocal()

    hadiths = (
        session.query(Hadith)
        .offset(skip)
        .limit(limit)
        .all()
    )

    session.close()
    return hadiths


@app.get("/hadiths/{hadith_id}", response_model=list[HadithResponse])
def get_hadith(hadith_id: int):
    session = SessionLocal()

    hadith = session.get(Hadith, hadith_id)

    if hadith is None:
        session.close()
        raise HTTPException(status_code=404, detail="Hadith not found")

    session.close()
    return hadith