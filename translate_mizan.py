import sqlite3
import time
from deep_translator import GoogleTranslator
from tqdm import tqdm

DB_PATH = "database/sqlite/mizan.db"
BATCH_SIZE = 50  # Simpan ke database setiap 50 hadis
SLEEP_TIME = 0.2 # Jeda 0.2 detik per hadis agar tidak di-block server penerjemah

print("📦 Membuka database mizan.db...")
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Ambil data yang translation_en ada isinya, tapi translation_id masih kosong/sama dengan translation_en
cursor.execute("""
    SELECT book_id, hadith_number, translation_en 
    FROM hadiths 
    WHERE translation_en IS NOT NULL 
      AND translation_en != '' 
      AND (translation_id IS NULL OR translation_id = '' OR translation_id = translation_en)
""")

rows = cursor.fetchall()
total_rows = len(rows)

print(f"🔍 Ditemukan {total_rows} hadis yang siap diterjemahkan ke Bahasa Indonesia.\n")

if total_rows == 0:
    print("✅ Semua hadis sudah diterjemahkan!")
    conn.close()
    exit()

translator = GoogleTranslator(source='en', target='id')

translated_count = 0
batch_data = []

print("🚀 Memulai proses penerjemahan bertahap...")

for row in tqdm(rows, desc="Proses Penerjemahan", unit="hadis"):
    book_id, h_num, trans_en = row
    
    try:
        # Jika teks terlalu panjang, pecah atau batasi agar tidak error
        text_to_translate = trans_en[:4500] 
        trans_id = translator.translate(text_to_translate)
    except Exception as e:
        # Jika gagal translate 1 item, gunakan teks asli agar tidak crash
        trans_id = trans_en
        time.sleep(1)

    batch_data.append((trans_id, book_id, h_num))
    translated_count += 1

    # Simpan ke DB setiap mencapai BATCH_SIZE
    if len(batch_data) >= BATCH_SIZE:
        cursor.executemany("""
            UPDATE hadiths 
            SET translation_id = ? 
            WHERE book_id = ? AND hadith_number = ?
        """, batch_data)
        conn.commit()
        batch_data = []

    time.sleep(SLEEP_TIME)

# Commit sisa batch terakhir jika ada
if batch_data:
    cursor.executemany("""
        UPDATE hadiths 
        SET translation_id = ? 
        WHERE book_id = ? AND hadith_number = ?
    """, batch_data)
    conn.commit()

print(f"\n✅ SUKSES! Berhasil menerjemahkan {translated_count} hadis ke Bahasa Indonesia di mizan.db.")
conn.close()
