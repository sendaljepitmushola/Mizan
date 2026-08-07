async function searchHadiths(query) {
    if (!query) return [];
    try {
        const response = await fetch('/api/v1/search?q=' + encodeURIComponent(query), {
            headers: {
                'Accept': 'application/json'
            }
        });
        if (!response.ok) {
            console.error('HTTP Status Error:', response.status);
            return [];
        }
        const data = await response.json();
        return data.results || data.data || [];
    } catch (error) {
        console.error('Fetch Error:', error);
        return [];
    }
}

async function getBooks() {
    try {
        const response = await fetch('/api/v1/books');
        if (!response.ok) return [];
        const data = await response.json();
        return data.data || data.books || [];
    } catch (error) {
        console.error('Fetch Error:', error);
        return [];
    }
}
