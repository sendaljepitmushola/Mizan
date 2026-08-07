document.addEventListener('DOMContentLoaded', async () => {
    const urlParams = new URLSearchParams(window.location.search);
    const query = urlParams.get('q') || urlParams.get('query') || '';
    
    // Set isi kolom input pencarian
    document.querySelectorAll('input[type="text"], input[type="search"]').forEach(input => {
        if (query) input.value = query;
    });

    if (query) {
        const results = await searchHadiths(query);
        renderResults(results);
    }
});

function renderResults(hadiths) {
    const container = document.getElementById('hadith-container') || 
                      document.getElementById('results') || 
                      document.querySelector('.hadith-list') || 
                      document.getElementById('hadiths-list');

    if (!container) return;

    if (!hadiths || hadiths.length === 0) {
        container.innerHTML = '<div class="text-center p-5 text-muted">Data tidak ditemukan atau backend belum merespon.</div>';
        return;
    }

    container.innerHTML = hadiths.map(h => {
        // Tampilkan terjemahan Bahasa Indonesia dari SQLite
        const translationText = h.translation_id || h.translation || 'Terjemahan tidak tersedia';
        const bookName = h.book_name || h.book_id || 'Kitab Hadis';
        const hadithNum = h.hadith_number || h.number || '-';
        const arabicText = h.arabic || '';

        return `
            <div class="card mb-4 p-4 border rounded shadow-sm bg-white text-start">
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <span class="badge bg-primary">${bookName}</span>
                    <span class="text-muted small">No. ${hadithNum}</span>
                </div>
                ${arabicText ? `<div class="arabic-text text-end fs-4 mb-3" style="font-family: 'Amiri', serif; line-height: 2;">${arabicText}</div>` : ''}
                <div class="translation-text text-dark mb-3" style="white-space: pre-line;">${translationText}</div>
                <div class="text-muted small">✓ ID: #${h.id || h.hadith_id}</div>
            </div>
        `;
    }).join('');
}
