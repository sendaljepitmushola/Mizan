// Konfigurasi URL Backend (Relative Path agar tidak kena blokir CORS/Ports)
const BACKEND_URL = "";

// Fungsi untuk mengecek koneksi ke backend FastAPI
async function checkBackendConnection() {
    try {
        const response = await fetch(`${BACKEND_URL}/health`);
        if (response.ok) {
            console.log("✅ Terhubung ke Backend FastAPI Mizan");
            return true;
        }
    } catch (error) {
        console.warn("⚠️ Gagal terhubung ke backend via health check:", error);
    }
    return false;
}

// Fungsi utama pencarian hadis
async function searchHadith(query, limit = 10) {
    try {
        const response = await fetch(`${BACKEND_URL}/search?query=${encodeURIComponent(query)}&limit=${limit}`);
        if (!response.ok) {
            throw new Error(`HTTP Error: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error("Gagal melakukan pencarian:", error);
        throw error;
    }
}

// Export agar bisa dipakai di skrip frontend lain jika menggunakan module
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { BACKEND_URL, checkBackendConnection, searchHadith };
}