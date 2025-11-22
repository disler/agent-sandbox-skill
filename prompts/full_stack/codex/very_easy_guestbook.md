# Simple Guestbook

Build a classic guestbook. Leave a message, see all messages.

**Database**:
```sql
CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    message TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

**Features**:
- Form: Name + Message inputs
- Submit button
- Display all messages (newest first)
- Show name, message, and timestamp

**Build time: < 5 min**
