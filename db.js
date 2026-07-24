const sqlite3 = require('sqlite3').verbose();
const path = require('path');

const dbPath = path.join(__dirname, 'mizan_hadith.db');
const db = new sqlite3.Database(dbPath, (err) => {
    if (err) {
        console.error('Gagal terhubung ke database:', err.message);
    } else {
        console.log('✅ Terhubung ke database SQLite Mizan');
    }
});

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

    // Reset dan isi ulang data dummy agar dataset terbaru masuk
    db.get("SELECT COUNT(*) AS count FROM hadiths", (err, row) => {
        // Jika data masih sedikit (kurang dari 5), kita bersihkan lalu isi data baru
        if (row && row.count < 5) {
            console.log("📥 Memperbarui dan mengisi dataset hadis ke database...");
            
            db.run("DELETE FROM hadiths"); // Bersihkan data lama

            const stmt = db.prepare(`
                INSERT INTO hadiths (book_slug, book_name, number, arabic, translation, narrator, grade)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            `);

            const sampleHadiths = [
                {
                    book_slug: 'bukhari',
                    book_name: 'Sahih Bukhari',
                    number: 1,
                    arabic: 'إِنَّمَا الأَعْمَالُ بِالنِّيَّاتِ، وَإِنَّمَا لِكُلِّ امْرِئٍ مَا نَوَى',
                    translation: 'Sesungguhnya setiap amalan tergantung pada niatnya, dan setiap orang akan mendapatkan sesuai dengan apa yang diniatkannya.',
                    narrator: 'Umar bin Khattab RA',
                    grade: 'Shahih'
                },
                {
                    book_slug: 'muslim',
                    book_name: 'Sahih Muslim',
                    number: 1,
                    arabic: 'الإِيمَانُ أَنْ تُؤْمِنَ بِاللَّهِ وَمَلاَئِكَتِهِ وَكُتُبِهِ وَرُسُلِهِ وَالْيَوْمِ الآخِرِ وَتُؤْمِنَ بِالْقَدَرِ خَيْرِهِ وَشَرِّهِ',
                    translation: 'Iman itu adalah engkau beriman kepada Allah, malaikat-malaikat-Nya, kitab-kitab-Nya, rasul-rasul-Nya, hari akhir, dan beriman kepada takdir yang baik maupun yang buruk.',
                    narrator: 'Umar bin Khattab RA',
                    grade: 'Shahih'
                },
                {
                    book_slug: 'bukhari',
                    book_name: 'Sahih Bukhari',
                    number: 13,
                    arabic: 'لاَ يُؤْمِنُ أَحَدُكُمْ حَتَّى يُحِبَّ لأَخِيهِ مَا يُحِبُّ لِنَفْسِهِ',
                    translation: 'Tidak beriman salah seorang di antara kamu hingga ia mencintai saudaranya sebagaimana ia mencintai dirinya sendiri.',
                    narrator: 'Anas bin Malik RA',
                    grade: 'Shahih'
                },
                {
                    book_slug: 'muslim',
                    book_name: 'Sahih Muslim',
                    number: 223,
                    arabic: 'الطَّهُورُ شَطْرُ الإِيمَانِ',
                    translation: 'Bersuci (kebersihan) itu adalah sebagian dari iman.',
                    narrator: 'Abu Malik Al-Asy\'ari RA',
                    grade: 'Shahih'
                },
                {
                    book_slug: 'tirmidzi',
                    book_name: 'Jami\' at-Tirmidzi',
                    number: 2646,
                    arabic: 'مَنْ سَلَكَ طَرِيقًا يَلْتَمِسُ فِيهِ عِلْمًا سَهَّلَ اللَّهُ لَهُ بِهِ طَرِيقًا إِلَى الْجَنَّةِ',
                    translation: 'Barangsiapa menempuh jalan untuk mencari ilmu, maka Allah akan memudahkan baginya jalan menuju surga.',
                    narrator: 'Abu Hurairah RA',
                    grade: 'Hasan Shahih'
                },
                {
                    book_slug: 'abudawud',
                    book_name: 'Sunan Abu Dawud',
                    number: 4799,
                    arabic: 'إِنَّمَا بُعِثْتُ لأُتَمِّمَ صَالِحَ الأَخْلاَقِ',
                    translation: 'Sesungguhnya aku diutus hanya untuk menyempurnakan akhlak yang mulia.',
                    narrator: 'Abu Hurairah RA',
                    grade: 'Shahih'
                },
                {
                    book_slug: 'bukhari',
                    book_name: 'Sahih Bukhari',
                    number: 5027,
                    arabic: 'خَيْرُكُمْ مَنْ تَعَلَّمَ الْقُرْآنَ وَعَلَّمَهُ',
                    translation: 'Sebaik-baik kalian adalah orang yang mempelajari Al-Qur\'an dan mengajarkannya.',
                    narrator: 'Utsman bin Affan RA',
                    grade: 'Shahih'
                }
            ];

            sampleHadiths.forEach(h => {
                stmt.run(h.book_slug, h.book_name, h.number, h.arabic, h.translation, h.narrator, h.grade);
            });

            stmt.finalize();
            console.log("✅ Dataset sampel hadis berhasil di-update.");
        }
    });
});

module.exports = db;