import os
import shutil
import sqlite3
import chromadb
from sentence_transformers import SentenceTransformer

# 1. Tentukan lokasi database SQLite
db_file = "./database/sqlite/mizan.db"
if not os.path.exists(db_file):
    db_file = "mizan_hadith.db"

print(f"📂 Menggunakan database SQLite: {db_file}")

# 2. Load Model Embedding Multilingual
print("📦 Memuat model AI Embedding (paraphrase-multilingual-MiniLM-L12-v2)...")
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

# 3. Reset database ChromaDB
chroma_path = "./chroma_db"
if os.path.exists(chroma_path):
    print("🧹 Menghapus ChromaDB lama...")
    shutil.rmtree(chroma_path)

chroma_client = chromadb.PersistentClient(path=chroma_path)
collection = chroma_client.create_collection(
    name="hadiths_vector",
    metadata={"hnsw:space": "cosine"}
)

# 4. Ambil dan Filter Data dari SQLite
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Deteksi tabel data hadis
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [t[0] for t in cursor.fetchall() if t[0] != 'sqlite_sequence']

table_name = "hadiths"
if "hadiths" in tables:
    table_name = "hadiths"
elif "hadith" in tables:
    table_name = "hadith"
else:
    for t in tables:
        if t != "books":
            table_name = t
            break

print(f"📊 Mengambil data dari tabel: '{table_name}'")

# Ambil informasi kolom
cursor.execute(f"PRAGMA table_info({table_name});")
columns = [info[1] for info in cursor.fetchall()]

cursor.execute(f"SELECT * FROM {table_name}")
rows = cursor.fetchall()

documents = []
metadatas = []
ids = []

print(f"⚡ Menyaring & memproses {len(rows)} data hadis...")

skipped_count = 0

for idx, row in enumerate(rows):
    row_dict = dict(zip(columns, row))
    
    h_id = str(row_dict.get('id') or row_dict.get('hadith_id') or idx + 1)
    h_num = str(row_dict.get('hadith_number') or row_dict.get('number') or row_dict.get('no') or '-')
    book = str(row_dict.get('book_id') or row_dict.get('book_name') or row_dict.get('kitab') or 'Kitab')
    
    arab = str(row_dict.get('arabic') or row_dict.get('arab') or '').strip()
    trans_id = str(row_dict.get('translation_id') or row_dict.get('translation') or row_dict.get('terjemah') or row_dict.get('indonesia') or '').strip()
    trans_en = str(row_dict.get('translation_en') or row_dict.get('terjemah_en') or '').strip()

    # --- FILTER KETAT ---
    # Buang hadis jika terjemahan Indonesia kosong atau tidak valid
    if not trans_id or trans_id.lower() == "terjemahan tidak tersedia" or len(trans_id) < 3:
        skipped_count += 1
        continue

    # Vektor dibuat khusus fokus pada Terjemahan Indonesia
    text_to_embed = f"{trans_id} {arab}".strip()

    documents.append(text_to_embed)
    metadatas.append({
        "hadith_id": h_id,
        "hadith_number": h_num,
        "book_id": book,
        "arabic": arab,
        "translation_en": trans_en,
        "translation_id": trans_id
    })
    ids.append(f"hadith_{h_id}_{idx}")

print(f"🚫 Berhasil membuang {skipped_count} hadis tanpa terjemahan Indonesia.")
print(f"✅ Total hadis berkualitas tinggi yang akan di-index: {len(documents)}")

# 5. Buat Embedding & Simpan ke ChromaDB
batch_size = 256
total_docs = len(documents)

for i in range(0, total_docs, batch_size):
    batch_docs = documents[i:i+batch_size]
    batch_meta = metadatas[i:i+batch_size]
    batch_ids = ids[i:i+batch_size]
    
    embeddings = model.encode(batch_docs).tolist()
    
    collection.add(
        embeddings=embeddings,
        documents=batch_docs,
        metadatas=batch_meta,
        ids=batch_ids
    )
    print(f"✅ Tersimpan {min(i+batch_size, total_docs)}/{total_docs} hadis")

print("\n🎉 Re-indexing Selesai! ChromaDB sekarang 100% berisi hadis berterjemahan Indonesia.")