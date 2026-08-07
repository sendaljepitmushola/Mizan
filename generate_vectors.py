import os
import glob
import sqlite3
import chromadb
from sentence_transformers import SentenceTransformer

def find_sqlite_db():
    primary_db = "database/sqlite/mizan.db"
    if os.path.exists(primary_db):
        return primary_db

    db_files = glob.glob("**/*.db", recursive=True) + glob.glob("**/*.sqlite*", recursive=True)
    db_files = [f for f in db_files if not "chroma" in f and not "venv" in f]
    return db_files[0] if db_files else None

def run():
    db_path = find_sqlite_db()
    if not db_path:
        print("❌ Database SQLite tidak ditemukan!")
        return

    print(f"📂 Menggunakan database: {db_path}")
    
    print("📦 Memuat model embedding AI...")
    model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    
    # Hapus koleksi vektor lama yang korup/mismatch
    try:
        chroma_client.delete_collection(name="hadiths_vector")
    except Exception:
        pass

    collection = chroma_client.create_collection(name="hadiths_vector")

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Query eksplisit mengambil kolom pasti dari tabel hadiths
    print("📊 Membaca tabel 'hadiths'...")
    cursor.execute("""
        SELECT id, book_id, chapter_id, hadith_number, arabic, translation_id 
        FROM hadiths 
        WHERE translation_id IS NOT NULL AND TRIM(translation_id) != ''
    """)
    rows = cursor.fetchall()

    if not rows:
        print("⚠️ Data hadis kosong.")
        return

    print(f"🔄 Memproses {len(rows)} data hadis...")

    documents = []
    metadatas = []
    ids = []

    for row in rows:
        row_id = str(row["id"])
        h_num = str(row["hadith_number"])
        h_arabic = str(row["arabic"] or "")
        h_trans = str(row["translation_id"])
        b_id = str(row["book_id"])

        documents.append(h_trans)
        ids.append(row_id)  # ID Unik menggunakan Primary Key DB
        metadatas.append({
            "hadith_id": row_id,
            "hadith_number": h_num,
            "book_id": b_id,
            "arabic": h_arabic,
            "translation_id": h_trans
        })

    print(f"⚡ Mengubah {len(documents)} terjemahan ke bentuk vektor & menyimpan ke ChromaDB...")
    
    # Batch processing per 1000 item
    batch_size = 1000
    total_docs = len(documents)

    for i in range(0, total_docs, batch_size):
        end_idx = min(i + batch_size, total_docs)
        print(f"   ⏳ Memproses Batch {i // batch_size + 1} ({i + 1} - {end_idx} dari {total_docs})...")
        
        batch_docs = documents[i:end_idx]
        batch_ids = ids[i:end_idx]
        batch_metas = metadatas[i:end_idx]

        embeddings = model.encode(batch_docs, show_progress_bar=False)

        collection.add(
            ids=batch_ids,
            embeddings=embeddings.tolist(),
            documents=batch_docs,
            metadatas=batch_metas
        )

    print("✅ SUKSES! File vektor berhasil dibuat ulang dengan sinkronisasi 100% tepat.")
    conn.close()

if __name__ == "__main__":
    run()