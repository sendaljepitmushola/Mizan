import os
import glob
import json
import sqlite3

def reset_and_import_english():
    db_path = "database/sqlite/mizan.db"
    
    # Pastikan folder database ada
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    print(f"📂 Menghubungkan dan mereset database: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Hapus tabel lama jika ada agar bersih dari data ID yang salah
    cursor.execute("DROP TABLE IF EXISTS hadiths;")

    # Buat ulang tabel
    cursor.execute("""
        CREATE TABLE hadiths (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id TEXT,
            chapter_id TEXT,
            hadith_number TEXT,
            arabic TEXT,
            translation_en TEXT,
            translation_id TEXT,
            UNIQUE(book_id, hadith_number) ON CONFLICT REPLACE
        );
    """)

    raw_dir = "database/raw/datasets/hadith-json/db"
    json_files = glob.glob(f"{raw_dir}/**/*.json", recursive=True)

    if not json_files:
        print(f"❌ Tidak ditemukan file JSON di {raw_dir}")
        return

    print(f"📚 Ditemukan {len(json_files)} file JSON. Memulai impor teks Bahasa Inggris...")

    total_inserted = 0

    for file_path in json_files:
        path_parts = file_path.split(os.sep)
        book_id = path_parts[-2] if len(path_parts) >= 2 else "general"
        chapter_file = os.path.basename(file_path).replace('.json', '')

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                items = data if isinstance(data, list) else data.get("hadiths", data.get("data", []))

                rows_to_insert = []
                for idx, item in enumerate(items, 1):
                    # Ambil nomor hadis
                    h_num = str(item.get("idInBook", item.get("id", idx)))
                    h_arab = item.get("arabic", "")
                    
                    # Ambil terjemahan Bahasa Inggris dari objek english
                    eng_obj = item.get("english", {})
                    if isinstance(eng_obj, dict):
                        narrator = eng_obj.get("narrator", "")
                        text = eng_obj.get("text", "")
                        h_trans_en = f"{narrator}\n{text}".strip()
                    else:
                        h_trans_en = str(eng_obj) if eng_obj else ""

                    if h_arab or h_trans_en:
                        rows_to_insert.append((
                            book_id,
                            chapter_file,
                            h_num,
                            h_arab,
                            h_trans_en,
                            "" # translation_id dibiarkan kosong dulu
                        ))

                if rows_to_insert:
                    cursor.executemany("""
                        INSERT OR REPLACE INTO hadiths (book_id, chapter_id, hadith_number, arabic, translation_en, translation_id)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, rows_to_insert)
                    total_inserted += len(rows_to_insert)

        except Exception as e:
            print(f"⚠️ Gagal membaca {file_path}: {e}")

    conn.commit()
    conn.close()
    print(f"\n✅ REFRESH SUKSES! Total {total_inserted} hadis berhasil dimasukkan dengan Bahasa Inggris yang akurat.")

if __name__ == "__main__":
    reset_and_import_english()