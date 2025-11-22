# Plan: Simple Calculator Full-Stack Application

## Task Description
Build a minimal full-stack calculator application with basic arithmetic operations (addition, subtraction, multiplication, division) that persists calculation history to a database. The application consists of:
- **Frontend**: Vite + Vue 3 + TypeScript + Pinia
- **Backend**: FastAPI + uvicorn + Python (uv)
- **Database**: SQLite

## Objective
Create a working full-stack calculator where users can perform arithmetic operations through a clean UI, see results instantly, and view calculation history that persists across sessions. The complete system includes a Vue 3 frontend, FastAPI backend with three endpoints, and SQLite database for history persistence.

## Relevant Files
Use these files and directories to complete the task (frontend and backend must remain separated):

### New Files
- `client/` - Vue 3 + TypeScript + Vite frontend application
  - `client/src/App.vue` - Main calculator component with UI
  - `client/src/components/Calculator.vue` - Calculator display and buttons
  - `client/src/components/History.vue` - Calculation history panel
  - `client/src/stores/calculator.ts` - Pinia store for state management
  - `client/src/services/api.ts` - API client for backend communication
  - `client/vite.config.ts` - Vite configuration with port 5173
  - `client/package.json` - Frontend dependencies
  - `client/index.html` - Entry HTML with title "multiport-test-2-calculator Calculator App"
- `server/` - FastAPI + Python backend application
  - `server/src/app.py` - Main FastAPI application with routes
  - `server/src/models.py` - SQLAlchemy database models
  - `server/src/database.py` - Database connection and session management
  - `server/src/schemas.py` - Pydantic models for request/response validation
  - `server/pyproject.toml` - Backend dependencies (uv managed)
  - `server/calculator.db` - SQLite database file
- Shared:
  - Root `.env` (if API keys needed) - not required for this simple app

### Dependencies
- **Frontend**:
  - `npm create vite@latest client -- --template vue-ts`
  - `npm install` (in client directory)
  - `npm install pinia` (state management)
  - `npm install axios` (HTTP client)
- **Backend**:
  - `uv init --app` (in server directory)
  - `uv add fastapi uvicorn[standard] sqlalchemy aiosqlite pydantic python-multipart`
  - `uv add --dev pytest httpx`
- **Database**:
  - SQLite (built into Python, no additional installation)
  - `uv add sqlalchemy aiosqlite` (already included above)
- **Shared/Tooling**:
  - CORS middleware (fastapi.middleware.cors.CORSMiddleware)

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### 1. Bootstrap & Verify Stack
- Create `/home/user/calculator-app` as the root project directory
- Create frontend: `/home/user/calculator-app/client` using `npm create vite@latest client -- --template vue-ts`
- Create backend: `/home/user/calculator-app/server` using `uv init --app`
- Configure Vite to run on port 5173 with `0.0.0.0` host for external access
- Configure FastAPI to run on port 8000 with `0.0.0.0` host and CORS enabled
- Update `client/index.html` title to "multiport-test-2-calculator Calculator App"
- Install all dependencies (npm install in client, uv sync in server)
- Verify both services start: backend on 8000, frontend on 5173

### 2. Backend & Database Foundation
- Design database schema: `calculations` table with columns: id (INTEGER PRIMARY KEY), expression (TEXT), result (REAL), timestamp (DATETIME)
- Create `server/src/database.py` with SQLAlchemy async engine and session factory
- Create `server/src/models.py` with `Calculation` model matching schema
- Initialize database with table creation on app startup
- Create `server/src/schemas.py` with Pydantic models:
  - `CalculateRequest(expression: str)`
  - `CalculateResponse(id: int, expression: str, result: float, timestamp: datetime)`
  - `HistoryResponse(id: int, expression: str, result: float, timestamp: datetime)`
- Implement FastAPI app structure in `server/src/app.py` with CORS middleware allowing all origins

### 3. Backend API Implementation
- **POST /api/calculate**:
  - Accept `CalculateRequest` with expression string
  - Validate expression contains only numbers, spaces, and operators (+, -, *, /)
  - Safely evaluate using Python's `eval()` with restricted globals
  - Save calculation to database with result and timestamp
  - Return `CalculateResponse` with id, expression, result, timestamp
- **GET /api/history**:
  - Query all calculations from database ordered by timestamp DESC
  - Return array of `HistoryResponse` objects
- **DELETE /api/history**:
  - Delete all records from calculations table
  - Return success message: `{"message": "History cleared"}`
- Add error handling for invalid expressions, division by zero, and database errors

### 4. Frontend Foundation
- Configure Vite with `vite.config.ts`:
  - Set server port to 5173
  - Set server host to `0.0.0.0` for external access
  - Configure proxy for `/api` to `http://localhost:8000/api`
- Create `client/src/services/api.ts`:
  - Base URL configuration pointing to `/api`
  - `calculate(expression: string)` function
  - `getHistory()` function
  - `clearHistory()` function
  - Error handling for network failures
- Setup Pinia store in `client/src/stores/calculator.ts`:
  - State: currentExpression, currentResult, history array
  - Actions: appendToExpression, calculate, clearExpression, loadHistory, clearHistory
  - Integrate with API service

### 5. Frontend UI Implementation
- Create `client/src/components/Calculator.vue`:
  - Display screen showing currentExpression and currentResult
  - Number pad grid (0-9) using CSS Grid
  - Operation buttons (+, -, *, /)
  - Equals button (=) to trigger calculation
  - Clear button (C) to reset display
  - Handle button clicks to build expression
  - Call Pinia store actions
  - Modern dark theme calculator styling
- Create `client/src/components/History.vue`:
  - Scrollable panel displaying calculation history
  - Each entry shows expression, result, and timestamp
  - Clear history button
  - Auto-refresh on new calculation
  - Responsive styling
- Update `client/src/App.vue`:
  - Layout with calculator and history side by side
  - Responsive design for mobile/desktop
  - Load history on component mount
  - Professional styling with modern color palette

### 6. Integration & Observability
- Connect frontend to backend with real API calls
- Handle loading states during API requests
- Display error messages for failed calculations
- Add console logging for debugging in both frontend and backend
- Ensure CORS is properly configured for cross-origin requests
- Test frontend-to-backend-to-database flow

### 7. Testing & Verification
- **Backend Tests**:
  - Start backend: `cd /home/user/calculator-app/server && uv run uvicorn src.app:app --host 0.0.0.0 --port 8000`
  - Test calculate endpoint: `curl -X POST http://localhost:8000/api/calculate -H "Content-Type: application/json" -d '{"expression":"5 + 3"}'`
  - Test history endpoint: `curl http://localhost:8000/api/history`
  - Test clear history: `curl -X DELETE http://localhost:8000/api/history`
  - Verify database: `sqlite3 /home/user/calculator-app/server/calculator.db "SELECT * FROM calculations;"`
- **Database Tests**:
  - Verify table exists: `sqlite3 /home/user/calculator-app/server/calculator.db ".schema calculations"`
  - Check data persistence after server restart
- **Frontend Tests**:
  - Start frontend: `cd /home/user/calculator-app/client && npm run dev -- --host 0.0.0.0 --port 5173`
  - Build frontend: `cd /home/user/calculator-app/client && npm run build`
  - Verify no build errors
- **Full-System Tests**:
  - Start both services (backend on 8000, frontend on 5173)
  - Open browser to frontend URL
  - Click: 5 + 3 = → verify result is 8
  - Click: 10 - 2 = → verify result is 8
  - Check history panel shows both calculations
  - Refresh page → verify history persists
  - Click clear history → verify history is cleared
  - Click clear button (C) → verify display resets to 0

## Acceptance Criteria
- Backend API runs on port 8000 and responds to all three endpoints
- SQLite database persists calculations with expression, result, and timestamp
- Frontend UI displays on port 5173 with modern calculator interface
- Number buttons (0-9) and operation buttons (+, -, *, /) build expressions correctly
- Equals button sends expression to backend and displays result
- History panel displays past calculations from database
- Clear button resets calculator display
- Clear history button removes all calculations from database
- Calculations persist across page refreshes and server restarts
- CORS is properly configured for frontend-backend communication
- No console errors in browser or server logs
- Application works end-to-end: user input → backend calculation → database storage → UI update

## Validation Commands
Execute these commands to validate the task is complete:

**Backend Validation**:
```bash
# Start backend server
cd /home/user/calculator-app/server
uv run uvicorn src.app:app --host 0.0.0.0 --port 8000 &

# Test calculate endpoint
curl -X POST http://localhost:8000/api/calculate -H "Content-Type: application/json" -d '{"expression":"5 + 3"}'

# Test history endpoint
curl http://localhost:8000/api/history

# Test clear history
curl -X DELETE http://localhost:8000/api/history
```

**Database Validation**:
```bash
# Check database schema
sqlite3 /home/user/calculator-app/server/calculator.db ".schema calculations"

# Query calculations
sqlite3 /home/user/calculator-app/server/calculator.db "SELECT * FROM calculations;"
```

**Frontend Validation**:
```bash
# Build frontend
cd /home/user/calculator-app/client
npm run build

# Start frontend dev server
npm run dev -- --host 0.0.0.0 --port 5173
```

**Full-Stack Validation**:
```bash
# Start both services in background
cd /home/user/calculator-app/server && uv run uvicorn src.app:app --host 0.0.0.0 --port 8000 &
cd /home/user/calculator-app/client && npm run dev -- --host 0.0.0.0 --port 5173 &

# Test from external URL (after exposing via E2B get-host)
curl https://5173-<sandbox-id>.e2b.app
```

## Notes
- The backend uses `eval()` with input validation - in production, use a safer expression parser like `ast.literal_eval` or a dedicated library
- CORS is configured to allow all origins for development - restrict this in production
- SQLite is suitable for this simple app - for production with multiple concurrent users, consider PostgreSQL
- The frontend uses Vite's dev server for development - for production, build and serve the static files
- Both frontend and backend must listen on `0.0.0.0` to be accessible from external URLs in E2B sandbox
- The HTML page title must start with "multiport-test-2-calculator" to track the workflow
- Port 5173 is the standard for Vite and should be used for consistency
- The application is designed to be simple and educational, demonstrating full-stack integration without unnecessary complexity
