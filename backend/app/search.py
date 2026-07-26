from sqlalchemy import func, or_
from .models import Hadith


def search_hadith(session, keyword: str, limit: int = 50):
    if not keyword or not keyword.strip():
        return []

    clean_keyword = keyword.strip().lower()

    # Menggunakan lower() pada kolom agar aman di SQLite
    return (
        session.query(Hadith)
        .filter(
            or_(
                func.lower(Hadith.translation_id).contains(clean_keyword),
                func.lower(Hadith.arabic).contains(clean_keyword),
            )
        )
        .limit(limit)
        .all()
    )