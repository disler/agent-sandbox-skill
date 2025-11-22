# Quick Poll

Build a simple single-question poll app. One question, multiple choice answers, show results as percentages.

**Database**:
```sql
CREATE TABLE poll (
    id INTEGER PRIMARY KEY,
    question TEXT,
    option_a TEXT,
    option_b TEXT,
    option_c TEXT,
    votes_a INTEGER DEFAULT 0,
    votes_b INTEGER DEFAULT 0,
    votes_c INTEGER DEFAULT 0
);
```

**Features**:
- Display question and 3 options
- Click option to vote
- Show results as percentages after voting
- Persist votes in database

## UI Design
Build a modern, professional interface with:
- Clean, minimal design with proper spacing
- Modern color palette (primary/secondary/accent colors)
- Responsive layout that works on mobile and desktop
- Professional typography (readable fonts, clear hierarchy)
- Smooth transitions and hover effects
- Consistent component styling throughout
- Proper form validation with user feedback
- Loading states for async operations

**Build time: < 5 min**
