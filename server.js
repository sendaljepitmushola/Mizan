const express = require('express');
const cors = require('cors');
const path = require('path');
require('dotenv').config();

const db = require('./db'); // Impor koneksi database

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

// Melayani file statis Frontend
app.use(express.static(path.join(__dirname, 'frontend')));

// Route Cek Status API
app.get('/api/status', (req, res) => {
    res.json({
        status: 'online',
        message: 'Project Mizan API Server Running!',
        timestamp: new Date()
    });
});

// Endpoint Pencarian Hadis API
app.get('/api/search', (req, res) => {
    const query = req.query.q || '';
    const book = req.query.book || '';

    let sql = `SELECT * FROM hadiths WHERE 1=1`;
    let params = [];

    if (query) {
        sql += ` AND (translation LIKE ? OR arabic LIKE ? OR narrator LIKE ?)`;
        const searchPattern = `%${query}%`;
        params.push(searchPattern, searchPattern, searchPattern);
    }

    if (book) {
        sql += ` AND book_slug = ?`;
        params.push(book);
    }

    db.all(sql, params, (err, rows) => {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        res.json({
            total: rows.length,
            query: query,
            book: book,
            results: rows
        });
    });
});

app.listen(PORT, () => {
    console.log(`=================================`);
    console.log(`🚀 Server Mizan Berjalan di http://localhost:${PORT}`);
    console.log(`=================================`);
});