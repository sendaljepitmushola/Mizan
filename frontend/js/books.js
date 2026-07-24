// Konfigurasi API Endpoint (sesuaikan jika URL backend berbeda)
const API_BASE_URL = 'http://localhost:8000/api';

// Fungsi untuk mengambil daftar kitab dari backend
async function fetchBooks() {
    try {
        const response = await fetch(`${API_BASE_URL}/books`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Gagal mengambil data kitab:', error);
        return null;
    }
}

// Fungsi helper untuk mendapatkan warna tema berdasarkan ID / Slug Kitab
function getBookTheme(bookId) {
    const themes = {
        bukhari: { bg: 'bg-emerald-900', border: 'border-emerald-700', btn: 'bg-emerald-700 hover:bg-emerald-800', text: 'text-emerald-600' },
        muslim: { bg: 'bg-slate-900', border: 'border-slate-700', btn: 'bg-mizan-navy hover:bg-slate-800', text: 'text-blue-600' },
        abudawud: { bg: 'bg-amber-900', border: 'border-amber-700', btn: 'bg-amber-700 hover:bg-amber-800', text: 'text-amber-700' },
        tirmidzi: { bg: 'bg-purple-950', border: 'border-purple-800', btn: 'bg-purple-800 hover:bg-purple-900', text: 'text-purple-700' },
        nasai: { bg: 'bg-teal-900', border: 'border-teal-700', btn: 'bg-teal-700 hover:bg-teal-800', text: 'text-teal-700' },
        ibnumajah: { bg: 'bg-red-950', border: 'border-red-800', btn: 'bg-red-800 hover:bg-red-900', text: 'text-red-700' }
    };

    return themes[bookId] || { bg: 'bg-slate-900', border: 'border-slate-700', btn: 'bg-mizan-navy hover:bg-slate-800', text: 'text-mizan-navy' };
}

// Inisialisasi saat dokumen selesai dimuat
document.addEventListener('DOMContentLoaded', async () => {
    console.log('Project Mizan: Books module initialized.');
    
    // Nanti logika merender data dari API secara otomatis dipanggil di sini:
    // const books = await fetchBooks();
});