const sqlite3 = require('sqlite3').verbose();
const path = require('path');

// Buat atau hubungkan ke file database SQLite
const dbPath = path.join(__dirname, 'mizan_hadith.db');
const db = new sqlite3.Database(dbPath, (err) => {
    if (err) {
        console.error('Gagal terhubung ke database:', err.message);
    } else {
        console.log('✅ Terhubung ke database SQLite Mizan');
    }
});

// Inisialisasi Tabel Hadis jika belum ada
db.serialize(() => {
    db.run(`
        CREATE TABLE IF NOT EXISTS hadiths (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_slug TEXT NOT NULL,
            book_name TEXT NOT NULL,
            number INTEGER NOT NULL,
            arabic TEXT NOT NULL,
            translation TEXT NOT NULL,
            narrator TEXT NOT NULL,
            grade TEXT DEFAULT 'Shahih'
        )
    `);

    // Masukkan data awal (sample) jika tabel masih kosong
    db.get("SELECT COUNT(*) AS count FROM hadiths", (err, row) => {
        if (row && row.count === 0) {
            console.log("📥 Mengisi sample data hadis ke database...");
            const stmt = db.prepare(`
                INSERT INTO hadiths (book_slug, book_name, number, arabic, translation, narrator, grade)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            `);

            stmt.run(
                'bukhari',
                'Sahih Bukhari',
                1,
                'إِنَّمَا الأَعْمَالُ بِالنِّيَّاتِ، وَإِنَّمَا لِكُلِّ امْرِئٍ مَا نَوَى',
                'Sesungguhnya setiap amalan tergantung pada niatnya, dan setiap orang akan mendapatkan sesuai dengan apa yang diniatkannya.',
                'Umar bin Khattab RA',
                'Shahih'
            );

            stmt.run(
                'muslim',
                'Sahih Muslim',
                1,
                'الإِيمَانُ أَنْ تُؤْمِنَ بِاللَّهِ وَمَلاَئِكَتِهِ وَكُتُبِهِ وَرُسُلِهِ وَالْيَوْمِ الآخِرِ وَتُؤْمِنَ بِالْقَدَرِ خَيْرِهِ وَشَرِّهِ',
                'Iman itu adalah engkau beriman kepada Allah, malaikat-malaikat-Nya, kitab-kitab-Nya, rasul-rasul-Nya, hari akhir, dan beriman kepada takdir yang baik maupun yang buruk.',
                'Umar bin Khattab RA',
                'Shahih'
            );

            stmt.finalize();
            console.log("✅ Sample data hadis berhasil dimasukkan.");
        }
    });
});

module.exports = db;