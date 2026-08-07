import sqlite3
import os

db_path = './database/sqlite/mizan.db'
os.makedirs('./database/sqlite', exist_ok=True)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Hapus tabel lama agar tidak bentrok skema/datatype
cursor.execute('DROP TABLE IF EXISTS hadiths')
cursor.execute('DROP TABLE IF EXISTS books')

# Buat tabel dengan skema yang bersih dan konsisten
cursor.execute('''
    CREATE TABLE books (
        id TEXT PRIMARY KEY,
        slug TEXT,
        title_en TEXT,
        title_ar TEXT,
        total_hadith INTEGER
    )
''')

cursor.execute('''
    CREATE TABLE hadiths (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        book_id TEXT,
        hadith_number TEXT,
        arabic TEXT,
        translation_id TEXT,
        translation_en TEXT
    )
''')

# Insert Metadata Buku
cursor.execute('''
    INSERT INTO books (id, slug, title_en, title_ar, total_hadith)
    VALUES ('bukhari', 'bukhari', 'Shahih Bukhari', 'صحيح البخاري', 7008)
''')

# Insert Hadis Niat Baku Resmi Bahasa Indonesia
data_hadis = [
    (
        'bukhari',
        '1',
        'حَدَّثَنَا عُمَرُ بْنُ الْخَطَّابِ رَضِيَ اللَّهُ عَنْهُ قَالَ: سَمِعْتُ رَسُولَ اللَّهِ صَلَّى اللَّهُ عَلَيْهِ وَسَلَّمَ يَقُولُ: إِنَّمَا الأَعْمَالُ بِالنِّيَّاتِ، وَإِنَّمَا لِكُلِّ امْرِئٍ مَا نَوَى، فَمَنْ كَانَتْ هِجْرَتُهُ إِلَى دُنْيَا يُصِيبُهَا، أَوْ إِلَى امْرَأَةٍ يَنْكِحُهَا، فَهِجْرَتُهُ إِلَى مَا هَاجَرَ إِلَيْهِ.',
        'Dari Umar bin Khattab radhiyallahu anhu, ia berkata: Saya mendengar Rasulullah shallallahu alaihi wa sallam bersabda: "Sesungguhnya setiap amalan tergantung pada niatnya, dan sesungguhnya setiap orang akan mendapatkan sesuai dengan apa yang ia niatkan. Barangsiapa yang hijrahnya karena dunia yang ingin diraihnya atau karena wanita yang ingin dinikahinya, maka hijrahnya adalah kepada apa yang ia hijrahkan."',
        'Narrated Umar bin Al-Khattab: I heard Allah\'s Messenger pbuh saying: The reward of deeds depends upon the intentions and every person will get the reward according to what he has intended...'
    ),
    (
        'bukhari',
        '2',
        'عَنْ عَائِشَةَ أُمِّ الْمُؤْمِنِينَ رَضِيَ اللَّهُ عَنْهَا أَنَّ الْحَارِثَ بْنَ هِشَامٍ رَضِيَ اللَّهُ عَنْهُ سَأَلَ رَسُولَ اللَّهِ صَلَّى اللَّهُ عَلَيْهِ وَسَلَّمَ فَقَالَ: يَا رَسُولَ اللَّهِ كَيْفَ يَأْتِيكَ الْوَحْيُ؟...',
        'Dari Aisyah Ummul Mukminin radhiyallahu anha, bahwa Al-Harits bin Hisham radhiyallahu anhu bertanya kepada Rasulullah SAW: "Wahai Rasulullah, bagaimana wahyu datang kepadamu?" Rasulullah SAW menjawab: "Kadang-kadang wahyu itu datang kepadaku bagaikan gemerincing lonceng, dan itulah yang paling berat bagiku..."',
        'Narrated Aishah: Al-Harith bin Hisham asked Allah\'s Messenger: O Allah\'s Messenger! How is the Divine Inspiration revealed to you?...'
    ),
    (
        'bukhari',
        '13',
        'عَنْ أَنَسٍ عَنِ النَّبِيِّ صَلَّى اللَّهُ عَلَيْهِ وَسَلَّمَ قَالَ: لاَ يُؤْمِنُ أَحَدُكُمْ حَتَّى يُحِبَّ لأَخِيهِ مَا يُحِبُّ لِنَفْسِهِ.',
        'Dari Anas radhiyallahu anhu, dari Nabi shallallahu alaihi wa sallam, beliau bersabda: "Tidak sempurna iman salah seorang di antara kalian hingga ia mencintai untuk saudaranya apa yang ia cintai untuk dirinya sendiri."',
        'Narrated Anas: The Prophet said: None of you will have faith till he wishes for his (Muslim) brother what he likes for himself.'
    )
]

cursor.executemany('''
    INSERT INTO hadiths (book_id, hadith_number, arabic, translation_id, translation_en)
    VALUES (?, ?, ?, ?, ?)
''', data_hadis)

conn.commit()
conn.close()
print("✅ BERHASIL! Database mizan.db sudah diperbaiki total dengan skema bersih & data baku.")
