# Simple Counter - Minimal Full-Stack App

Build the simplest possible full-stack application: a counter that persists to a database. One button to increment, one to decrement, and the count is saved.

## Value Proposition

The absolute minimum viable full-stack app. Tests that frontend, backend, and database all work together with the least possible complexity.

## Core Features

### Display
- Show current count as a large number
- Clean, centered UI

### Actions
- **Increment Button** (+1)
- **Decrement Button** (-1)
- **Reset Button** (back to 0)

### Persistence
- Count persists in SQLite database
- Survives page refresh
- Survives server restart

## Technical Requirements

### Database Schema
- Single table to store counter value
- ID field (primary key) and value field (integer)
- Initialize with default value of 0

### Backend API
**Two endpoints total**:

1. **GET /api/count** - Get current count
   - Returns: `{ "value": 0 }`

2. **POST /api/count** - Update count
   - Body: `{ "action": "increment" | "decrement" | "reset" }`
   - Returns: `{ "value": 1 }`

### Frontend
**Single component**:
- Display count in large font (48px+)
- Three buttons: `+`, `-`, `Reset`
- Fetch count on page load
- Update database on button click
- Show updated count immediately

## Implementation Details

### Database Setup
- Initialize a single counter table with ID and value columns
- Set initial counter value to 0

### Backend Logic
```
GET /api/count:
  - Query counter value from database
  - Return JSON with current value

POST /api/count:
  - Accept action parameter (increment, decrement, or reset)
  - Update database accordingly
  - Return updated counter value
```

### Frontend Component
- Display counter value in large font
- Implement three buttons for increment, decrement, and reset
- Use fetch API to communicate with backend
- Update UI with response from backend
- Style with CSS for centered layout

## Success Criteria

- [ ] Counter displays on page load
- [ ] Increment button increases count by 1
- [ ] Decrement button decreases count by 1
- [ ] Reset button sets count to 0
- [ ] Count persists after page refresh
- [ ] Count persists after server restart
- [ ] All three layers work (frontend ↔ backend ↔ database)

## Testing

### Manual Test Flow
1. Open app in browser
2. Click increment 3 times → should show 3
3. Refresh page → should still show 3
4. Click decrement once → should show 2
5. Click reset → should show 0
6. Restart backend server
7. Refresh page → should still show 0 (or last value before restart)

### Validation
```bash
# Backend test
curl http://localhost:8000/api/count

# Increment
curl -X POST http://localhost:8000/api/count \
  -H "Content-Type: application/json" \
  -d '{"action":"increment"}'

# Verify database
sqlite3 counter.db "SELECT * FROM counter"
```

## Why This Is Perfect

✅ **Minimal**: 1 table, 2 endpoints, 1 component
✅ **Fast**: Can build in under 5 minutes
✅ **Complete**: Tests entire full-stack pipeline
✅ **Observable**: Easy to verify it works
✅ **Debuggable**: Simple enough to troubleshoot instantly

This is the **ground zero** test case. If this doesn't build successfully, the workflow has fundamental issues. If it does build, the workflow is validated.

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

