# URL Shortener

Build a minimal URL shortener. Paste long URL, get short code, redirect works.

**Database**:
```sql
CREATE TABLE urls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    long_url TEXT NOT NULL,
    short_code TEXT UNIQUE NOT NULL,
    clicks INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

**Backend**:
- POST /api/shorten - Create short URL (generate 6-char code)
- GET /:code - Redirect to long URL (increment clicks)
- GET /api/stats/:code - Show click count

**Frontend**:
- Input field for long URL
- Submit button
- Display shortened URL (copyable)
- Show click count
- Clean simple, UI professional looking and functional.

**Build time: < 5 min**
