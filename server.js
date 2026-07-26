const express = require('express');
const path = require('path');
const sqlite3 = require('sqlite3').verbose();
const cors = require('cors');
const app = express();
const port = 8000; // Dikunci di 8000

app.use(cors());
app.use(express.static(path.join(__dirname, 'frontend')));

const dbPath = path.resolve(__dirname, 'database/sqlite/mizan.db');
const db = new sqlite3.Database(dbPath);

app.get('/hadiths/search', (req, res) => {
    const userInput = req.query.q;
    if (!userInput) return res.json([]);

    // Stopwords untuk membersihkan kalimat natural
    const stopwords = ['apakah', 'ada', 'hadis', 'tentang', 'mengenai', 'untuk', 'dari', 'yang', 'dan', 'carikan', 'keutamaan'];
    
    const words = userInput.toLowerCase()
        .replace(/[^\w\s]/g, "")
        .split(/\s+/)
        .filter(w => w.length > 2 && !stopwords.includes(w));

    if (words.length === 0) return res.json([]);

    // Logika OR: Mencari hadis yang mengandung SALAH SATU kata kunci
    let sql = `SELECT * FROM hadiths WHERE translation_id LIKE ?`;
    let params = [`%${words[0]}%`];

    for(let i = 1; i < words.length; i++) {
        sql += ` OR translation_id LIKE ?`;
        params.push(`%${words[i]}%`);
    }

    sql += ` LIMIT 15`;

    db.all(sql, params, (err, rows) => {
        if (err) return res.status(500).json({ error: err.message });
        res.json(rows);
    });
});

app.listen(port, () => {
    console.log(`🚀 Server Mizan berjalan di http://localhost:${port}`);
});