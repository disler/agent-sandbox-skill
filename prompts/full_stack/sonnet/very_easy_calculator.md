# Simple Calculator - Minimal Full-Stack App

Build a simple full-stack calculator application with basic arithmetic operations that persists calculation history to a database.

## Value Proposition

A minimal calculator that demonstrates full-stack integration with frontend, backend, and database persistence. Tests basic CRUD operations and API communication.

## Core Features

### Display
- Show current calculation result
- Display current expression being built
- Clean, centered calculator UI

### Actions
- **Number Buttons** (0-9)
- **Operation Buttons** (+, -, *, /)
- **Equals Button** (=) - Calculate result
- **Clear Button** (C) - Reset calculator
- **Calculation History** - View past calculations

### Persistence
- Save calculation history in SQLite database
- Each entry includes expression and result
- Survives page refresh

## Technical Requirements

### Database Schema
- Calculations table to store history
- Fields: id (primary key), expression (text), result (float), timestamp

### Backend API
**Three endpoints total**:

1. **POST /api/calculate** - Perform calculation
   - Body: `{ "expression": "5 + 3" }`
   - Returns: `{ "expression": "5 + 3", "result": 8 }`
   - Saves to database

2. **GET /api/history** - Get calculation history
   - Returns: `[{ "id": 1, "expression": "5 + 3", "result": 8, "timestamp": "..." }]`

3. **DELETE /api/history** - Clear history
   - Returns: `{ "message": "History cleared" }`

### Frontend
**Calculator component**:
- Display screen showing current expression and result
- Number pad (0-9)
- Operation buttons (+, -, *, /)
- Equals button to calculate
- Clear button to reset
- History panel showing past calculations
- Style as a modern calculator interface

## Implementation Details

### Database Setup
- Initialize calculations table with id, expression, result, and timestamp
- Auto-timestamp on insert

### Backend Logic
```
POST /api/calculate:
  - Validate expression
  - Evaluate safely (use Python's ast.literal_eval or similar)
  - Save expression + result to database
  - Return result

GET /api/history:
  - Query all calculations ordered by timestamp DESC
  - Return JSON array

DELETE /api/history:
  - Clear all records from calculations table
  - Return success message
```

### Frontend Component
- Calculator display showing expression and result
- Number buttons that append digits
- Operation buttons that append operators
- Equals button sends expression to backend
- Display result from backend
- History panel fetches and displays past calculations
- Clear button resets display
- Modern calculator styling with CSS Grid

## Success Criteria

- [ ] Calculator displays on page load
- [ ] Number buttons build expression
- [ ] Operation buttons work (+, -, *, /)
- [ ] Equals button calculates and displays result
- [ ] Calculation saves to database
- [ ] History displays past calculations
- [ ] Clear button resets calculator
- [ ] History persists after page refresh
- [ ] All three layers work (frontend ↔ backend ↔ database)

## Testing

### Manual Test Flow
1. Open app in browser
2. Click: 5 + 3 = → should show result 8
3. Click: 10 - 2 = → should show result 8
4. Check history panel → should show both calculations
5. Refresh page → history should still be there
6. Clear button → display resets to 0

### Validation
```bash
# Backend test
curl http://localhost:8000/api/history

# Calculate
curl -X POST http://localhost:8000/api/calculate \
  -H "Content-Type: application/json" \
  -d '{"expression":"5 + 3"}'

# Verify database
sqlite3 calculator.db "SELECT * FROM calculations"
```

## Why This Works

✅ **Simple**: Basic arithmetic only
✅ **Fast**: Can build in under 10 minutes
✅ **Complete**: Tests CRUD operations and API integration
✅ **Observable**: Easy to verify calculations are correct
✅ **Practical**: Real-world use case

## UI Design
Build a modern, professional calculator interface with:
- Clean, minimal design resembling a real calculator
- Modern color palette (dark theme calculator style)
- Responsive layout that works on mobile and desktop
- Professional typography (monospace for display, sans-serif for buttons)
- Button hover effects and click feedback
- Grid layout for calculator buttons
- History panel with scrollable list
- Clear visual separation between display, buttons, and history
- Loading states for async operations
