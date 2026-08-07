import sqlite3
import chromadb
from sentence_transformers import SentenceTransformer
import shutil
import os

print("1. Menghapus folder ChromaDB lama...")
if os.path.exists("./chroma_db"):
    shutil.rmtree("./chroma_db")

print("2. Memuat model AI Embedding...")
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

print("3. Membuka database SQLite mizan.db...")
conn = sqlite3.connect("database/sqlite/mizan.db")
cursor = conn.cursor()

cursor.execute("SELECT book_id, hadith_number, arabic, translation_en FROM hadiths WHERE translation_en != '' LIMIT 5000")
rows = cursor.fetchall()

print(f"4. Memproses {len(rows)} hadis ke ChromaDB...")

chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="hadiths_vector")

documents = []
metadatas = []
ids = []

for idx, row in enumerate(rows):
    book_id, h_num, arab, trans_en = row
    
    doc_text = f"{trans_en} {arab}"
    
    documents.append(doc_text)
    metadatas.append({
        "book_id": book_id,
        "hadith_number": h_num,
        "arabic": arab,
        "translation_en": trans_en,
        "translation_id": trans_en
    })
    ids.append(f"{book_id}_{h_num}_{idx}")

embeddings = model.encode(documents).tolist()

collection.add(
    documents=documents,
    embeddings=embeddings,
    metadatas=metadatas,
    ids=ids
)

print("\n✅ SUKSES! Database ChromaDB selesai dibuat ulang dari mizan.db.")
conn.close()
