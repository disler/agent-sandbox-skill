# Plan: Simple Counter - Minimal Full-Stack App

## Task Description
Build the simplest possible full-stack application: a counter that persists to a database. The app features one button to increment, one to decrement, and one to reset, with all values saved to SQLite. This plan uses the standardized stack:
- Frontend: Vite + Vue 3 + TypeScript + Pinia
- Backend: FastAPI + uvicorn + Python (uv)
- Database: SQLite

## Objective
Create a minimal viable full-stack application that demonstrates frontend ↔ backend ↔ database integration. When complete, users should be able to increment/decrement/reset a counter that persists across page refreshes and server restarts.

## Relevant Files
Use these files and directories to complete the task (frontend and backend must remain separated):

### New Files
- `frontend/src/App.vue` - Main counter UI component
- `frontend/src/stores/counter.ts` - Pinia store for counter state management
- `frontend/src/services/api.ts` - API client for backend communication
- `frontend/vite.config.ts` - Vite configuration with proxy for API calls
- `frontend/.env` - Environment variables for API base URL
- `backend/src/app.py` - FastAPI application with counter endpoints
- `backend/src/models.py` - SQLAlchemy models for counter table
- `backend/src/database.py` - Database connection and session management
- `backend/src/schemas.py` - Pydantic schemas for request/response validation
- `backend/counter.db` - SQLite database file (created at runtime)
- `backend/.env` - Backend environment variables (if needed for API keys)

### Dependencies
- Frontend:
  - `npm create vite@latest frontend -- --template vue-ts`
  - `cd frontend && npm install`
  - `npm install pinia`
  - `npm install axios`
- Backend:
  - `mkdir backend && cd backend`
  - `uv init --app`
  - `uv add fastapi uvicorn[standard]`
  - `uv add sqlalchemy`
  - `uv add pydantic`
  - `uv add --dev pytest httpx`
- Database:
  - SQLite (built-in with Python, no installation needed)
- Shared/Tooling:
  - CORS middleware configured in FastAPI for local development

## Implementation Phases

### Phase 1: Foundation
Scaffold frontend (Vite + Vue + TypeScript + Pinia) and backend (FastAPI + uv) projects. Initialize SQLite database schema. Configure environment variables and CORS. Run both services once to confirm they boot on their respective ports (frontend: 5173, backend: 8000).

### Phase 2: Core Implementation
Implement backend API endpoints for counter operations (GET /api/count, POST /api/count). Create SQLite table and SQLAlchemy models. Build frontend component with three buttons and display. Wire frontend store to API service layer.

### Phase 3: Integration & Polish
Connect frontend to live backend. Add error handling and loading states. Style UI with modern, clean design. Test persistence across refresh and restart. Validate end-to-end user flow.

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### 1. Bootstrap & Verify Stack
- Create frontend using Vite: `npm create vite@latest frontend -- --template vue-ts`
- Install frontend dependencies: `cd frontend && npm install && npm install pinia axios`
- Create backend directory and initialize uv project: `mkdir backend && cd backend && uv init --app`
- Install backend dependencies: `uv add fastapi uvicorn[standard] sqlalchemy pydantic && uv add --dev pytest httpx`
- Start backend dev server to verify: `cd backend && uv run uvicorn src.app:app --reload --port 8000` (should see "Application startup complete")
- Start frontend dev server to verify: `cd frontend && npm run dev` (should see Vite dev server on port 5173)

### 2. Backend & Database Foundation
- Design database schema: single `counter` table with `id` (primary key) and `value` (integer)
- Create `backend/src/database.py` with SQLite connection string and session management
- Create `backend/src/models.py` with SQLAlchemy Counter model
- Create `backend/src/schemas.py` with Pydantic schemas: CounterResponse, CounterUpdate
- Initialize database and seed with default counter value of 0 in app startup

### 3. Backend API Implementation
- Create `backend/src/app.py` with FastAPI app instance
- Configure CORS middleware to allow frontend origin (http://localhost:5173)
- Implement `GET /api/count` endpoint: query counter from database and return JSON
- Implement `POST /api/count` endpoint: accept action (increment/decrement/reset), update database, return new value
- Add database session dependency injection for endpoints
- Add error handling for database operations

### 4. Frontend Foundation
- Configure Pinia store in `frontend/src/main.ts`
- Create `frontend/src/services/api.ts` with axios client configured for backend URL
- Create `frontend/src/stores/counter.ts` with Pinia store: state (count, loading, error), actions (fetchCount, updateCount)
- Configure `frontend/vite.config.ts` with proxy to backend (/api -> http://localhost:8000/api)
- Create `frontend/.env` with `VITE_API_BASE_URL=http://localhost:8000`

### 5. Frontend UI Implementation
- Create `frontend/src/App.vue` with counter display and three buttons (+, -, Reset)
- Display counter value in large font (48px+) centered on page
- Implement click handlers that call store actions (increment, decrement, reset)
- Show loading state while API calls are in progress
- Show error messages if API calls fail
- Style with modern CSS: clean layout, hover effects, professional color palette

### 6. Integration & Configuration
- Ensure backend listens on `0.0.0.0` for external access (not just localhost)
- Configure frontend dev server to use `--host 0.0.0.0` for external access
- Test frontend → backend communication with real data
- Verify CORS headers are properly set
- Test persistence: increment counter, refresh page, verify value persists
- Test database persistence: restart backend, verify counter value persists

### 7. Testing & Verification
- Backend tests:
  - Unit test for database model creation and queries
  - Integration test for GET /api/count endpoint
  - Integration test for POST /api/count with all actions (increment/decrement/reset)
  - Test database initialization with default value
- Database tests:
  - Verify counter table exists with correct schema
  - Verify seed data (default value 0) is inserted on startup
  - Verify value persists across backend restarts
- Frontend tests:
  - Manual test: load page, verify counter displays
  - Manual test: click increment 3 times, verify shows 3
  - Manual test: refresh page, verify still shows 3
  - Manual test: click decrement, verify shows 2
  - Manual test: click reset, verify shows 0
- Full-system test:
  - Start backend: `cd backend && uv run uvicorn src.app:app --host 0.0.0.0 --port 8000`
  - Start frontend: `cd frontend && npm run dev -- --host 0.0.0.0 --port 5173`
  - Open browser to frontend URL
  - Execute complete user flow: increment, refresh, decrement, reset, verify persistence
  - Restart backend server, verify counter value persists

## Testing Strategy
- Backend: Unit tests for Counter model, integration tests for both API endpoints with test database, verify CRUD operations
- Database: Schema validation, seed data verification, persistence tests across restarts
- Frontend: Component tests would use Vitest but for this minimal app, manual testing of UI interactions is sufficient
- Combined: End-to-end manual test that starts both backend (port 8000) and frontend (port 5173), exercises all three button actions, and verifies persistence across refresh and server restart

## Acceptance Criteria
- ✅ Counter displays current value on page load
- ✅ Increment button increases count by 1 and updates database
- ✅ Decrement button decreases count by 1 and updates database
- ✅ Reset button sets count to 0 and updates database
- ✅ Counter value persists after page refresh
- ✅ Counter value persists after backend server restart
- ✅ Backend API responds to GET /api/count with current value
- ✅ Backend API responds to POST /api/count with updated value
- ✅ Database contains counter table with correct schema
- ✅ Frontend displays loading states during API calls
- ✅ Frontend displays error messages on API failures
- ✅ UI is modern, clean, and professionally styled
- ✅ Both services run on specified ports (backend: 8000, frontend: 5173)
- ✅ CORS is properly configured for local development

## Validation Commands
Execute these commands to validate the task is complete:

### Backend Validation
```bash
# Start backend server
cd backend
uv run uvicorn src.app:app --host 0.0.0.0 --port 8000 --reload

# In another terminal, test endpoints
curl http://localhost:8000/api/count
# Expected: {"value": 0}

curl -X POST http://localhost:8000/api/count \
  -H "Content-Type: application/json" \
  -d '{"action":"increment"}'
# Expected: {"value": 1}

curl -X POST http://localhost:8000/api/count \
  -H "Content-Type: application/json" \
  -d '{"action":"decrement"}'
# Expected: {"value": 0}

curl -X POST http://localhost:8000/api/count \
  -H "Content-Type: application/json" \
  -d '{"action":"reset"}'
# Expected: {"value": 0}

# Run backend tests
uv run pytest tests/ -v
```

### Database Validation
```bash
# Verify database file exists
ls backend/counter.db

# Check table schema (requires sqlite3 CLI)
sqlite3 backend/counter.db ".schema counter"
# Expected: CREATE TABLE counter (id INTEGER PRIMARY KEY, value INTEGER)

# Verify current value
sqlite3 backend/counter.db "SELECT * FROM counter"
# Expected: 1|<current_value>
```

### Frontend Validation
```bash
# Start frontend dev server
cd frontend
npm run dev -- --host 0.0.0.0 --port 5173

# Build frontend to verify no errors
npm run build
# Expected: Build completes successfully with no errors
```

### Full-Stack Validation
```bash
# Terminal 1: Start backend
cd backend && uv run uvicorn src.app:app --host 0.0.0.0 --port 8000

# Terminal 2: Start frontend
cd frontend && npm run dev -- --host 0.0.0.0 --port 5173

# Manual testing in browser:
# 1. Open frontend URL in browser
# 2. Verify counter displays (should show current value)
# 3. Click increment 3 times → verify shows 3
# 4. Refresh page → verify still shows 3
# 5. Click decrement → verify shows 2
# 6. Click reset → verify shows 0
# 7. Stop backend (Ctrl+C), restart it → verify counter persists
```

## Notes
- SQLite database file will be created automatically on first run in `backend/counter.db`
- The counter table will have a single row with id=1 that gets updated on each action
- CORS must be configured to allow requests from http://localhost:5173 during development
- For E2B sandbox deployment, backend must listen on 0.0.0.0 (not localhost) to be accessible
- Frontend dev server must also use --host 0.0.0.0 for external access
- The title of the HTML page should begin with "multiport-test-1-counter" for workflow identification
- This is a minimal test case to validate the complete full-stack pipeline
- Modern UI design: use clean spacing, professional color palette, smooth hover effects, responsive layout
