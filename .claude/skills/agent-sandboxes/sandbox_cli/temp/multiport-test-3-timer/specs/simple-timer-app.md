# Plan: Simple Timer Application

## Task Description
Create a simple, elegant countdown timer web application using Vite + Vue 3 + TypeScript + Pinia for the frontend, FastAPI + uvicorn + Python (uv) for the backend, and SQLite for the database. The app will allow users to set timers, start/stop/reset them, and save timer presets.

## Objective
Build a fully functional full-stack timer application where users can:
- Set custom countdown timers (hours, minutes, seconds)
- Start, pause, and reset timers
- Save and load timer presets (e.g., "Pomodoro 25min", "Break 5min")
- View timer history from the database
- Access the application through a responsive, visually appealing UI

## Problem Statement
Users need a simple, accessible web-based timer that can persist their favorite timer presets and track timer history without requiring installation of native apps.

## Solution Approach
The application uses a three-tier architecture:
1. **Frontend (Vue 3 + Pinia)**: Provides an interactive timer UI with real-time countdown display, controls, and preset management
2. **Backend (FastAPI)**: Exposes REST APIs for CRUD operations on timer presets and history records
3. **Database (SQLite)**: Persists timer presets and completed timer sessions

**Data Flow**:
- User creates/selects a timer preset → Frontend calls POST /api/presets → Backend saves to SQLite
- User starts a timer → Frontend manages countdown locally
- Timer completes → Frontend calls POST /api/history → Backend records session

## Relevant Files

### New Files
- **Frontend**:
  - `/home/user/client/src/App.vue` - Main app shell with timer display
  - `/home/user/client/src/components/TimerDisplay.vue` - Countdown display component
  - `/home/user/client/src/components/TimerControls.vue` - Start/pause/reset buttons
  - `/home/user/client/src/components/PresetManager.vue` - Save/load presets UI
  - `/home/user/client/src/stores/timer.ts` - Pinia store for timer state
  - `/home/user/client/src/services/api.ts` - API client for backend
  - `/home/user/client/vite.config.ts` - Vite config with proxy to backend
  - `/home/user/client/index.html` - HTML entry point (update title to "multiport-test-3-timer")

- **Backend**:
  - `/home/user/server/src/main.py` - FastAPI app with CORS and routes
  - `/home/user/server/src/models.py` - SQLAlchemy models for presets and history
  - `/home/user/server/src/schemas.py` - Pydantic schemas for validation
  - `/home/user/server/src/database.py` - Database connection and session management
  - `/home/user/server/src/crud.py` - CRUD operations for presets and history

- **Database**:
  - `/home/user/server/timer.db` - SQLite database file (auto-created)

### Dependencies

- **Frontend**:
  ```bash
  cd /home/user/client
  npm install pinia
  npm install axios
  npm install --save-dev @vitejs/plugin-vue
  ```

- **Backend**:
  ```bash
  cd /home/user/server
  uv add fastapi uvicorn[standard] sqlalchemy aiosqlite pydantic python-dotenv
  uv add --dev pytest httpx
  ```

- **Shared/Tooling**:
  - CORS configured in FastAPI to allow frontend requests
  - Environment variables for database path and API settings

## Implementation Phases

### Phase 1: Foundation
- Scaffold frontend (Vite + Vue 3 + TypeScript) and backend (FastAPI + uv) projects
- Initialize SQLite database with schema for timer presets and history
- Configure CORS and environment variables
- Verify both frontend (port 5173) and backend (port 8000) boot successfully

### Phase 2: Core Implementation
- Implement backend API endpoints for presets and history CRUD
- Create SQLAlchemy models and Pydantic schemas
- Build frontend timer logic with Pinia store
- Design UI components for timer display and controls

### Phase 3: Integration & Polish
- Connect frontend to backend APIs
- Add error handling and loading states
- Polish UI with smooth animations and clear feedback
- Add visual appeal with gradients and modern styling

## Step by Step Tasks

### 1. Bootstrap & Verify Stack
- Create `/home/user/client` directory and initialize Vite + Vue 3 + TypeScript project
- Create `/home/user/server` directory and initialize FastAPI project with uv
- Install all dependencies for both frontend and backend
- Start both servers to confirm they boot:
  - Backend: `cd /home/user/server && uv run uvicorn src.main:app --reload --port 8000`
  - Frontend: `cd /home/user/client && npm run dev -- --host 0.0.0.0 --port 5173`

### 2. Backend & Database Foundation
- Create SQLAlchemy models in `models.py`:
  - `TimerPreset` table: id, name, hours, minutes, seconds, created_at
  - `TimerHistory` table: id, preset_id, duration_seconds, completed_at
- Create database connection and session management in `database.py`
- Create Pydantic schemas in `schemas.py` for request/response validation
- Initialize database on app startup

### 3. Backend API Implementation
- Implement CRUD operations in `crud.py`:
  - Create, read, update, delete timer presets
  - Create and read timer history entries
- Create FastAPI routes in `main.py`:
  - `GET /api/presets` - List all presets
  - `POST /api/presets` - Create new preset
  - `GET /api/presets/{id}` - Get specific preset
  - `DELETE /api/presets/{id}` - Delete preset
  - `POST /api/history` - Record completed timer
  - `GET /api/history` - Get recent history
  - `GET /health` - Health check endpoint
- Configure CORS to allow requests from frontend (port 5173)

### 4. Frontend Foundation
- Create Pinia store (`stores/timer.ts`) with state:
  - Current timer values (hours, minutes, seconds)
  - Timer status (idle, running, paused)
  - Remaining time in seconds
  - Timer interval reference
- Create API service (`services/api.ts`) with axios for backend calls
- Configure Vite proxy to backend API in `vite.config.ts`
- Update `index.html` title to "multiport-test-3-timer"

### 5. Frontend Components
- Create `TimerDisplay.vue`:
  - Large, clear display of countdown (HH:MM:SS format)
  - Circular progress indicator
  - Visual feedback when timer completes (color change, animation)
- Create `TimerControls.vue`:
  - Input fields for hours, minutes, seconds
  - Start/Pause button (toggles based on state)
  - Reset button
  - Save Preset button
- Create `PresetManager.vue`:
  - List of saved presets with load and delete buttons
  - Form to name and save current timer as preset
  - Recent history list showing completed timers

### 6. Frontend Integration
- Wire up `App.vue` to use all components
- Connect Pinia actions to API service:
  - Load presets on mount
  - Save preset calls POST /api/presets
  - Delete preset calls DELETE /api/presets/{id}
  - Record completed timer calls POST /api/history
- Implement timer countdown logic:
  - Use setInterval for countdown
  - Update store state every second
  - Play sound/show notification when timer completes
  - Automatically record to history when completed

### 7. Styling & UX Polish
- Add modern, clean CSS with gradients and shadows
- Ensure text is highly readable (avoid poor color combinations)
- Add smooth transitions for button states and timer updates
- Make layout responsive for mobile and desktop
- Add loading states for API calls
- Add error messages for failed operations

### 8. Testing & Verification
- Backend tests:
  - Test all CRUD endpoints with pytest and httpx
  - Verify database operations and data integrity
  - Test CORS configuration
- Frontend tests:
  - Test timer countdown logic
  - Test preset save/load functionality
  - Test API integration
- Full-system test:
  - Start both servers
  - Create a preset, start timer, verify completion
  - Check database for saved preset and history
  - Verify all UI interactions work smoothly

## Testing Strategy

- **Backend**:
  - Unit tests for CRUD operations with in-memory SQLite
  - Integration tests for all API endpoints
  - Validate request/response schemas with Pydantic

- **Database**:
  - Schema validation tests
  - Data integrity checks for foreign keys
  - Test cascade deletes for preset history

- **Frontend**:
  - Component tests for timer logic
  - Store tests for state management
  - API service mocking tests

- **Combined**:
  - End-to-end test: Start both servers, create preset, run timer to completion, verify in database
  - Smoke test: Verify health endpoint and basic timer functionality
  - CORS validation: Ensure frontend can call backend APIs

## Acceptance Criteria

1. Backend API successfully handles all CRUD operations for presets and history
2. Frontend displays a working countdown timer with start/pause/reset functionality
3. Users can save timer presets with custom names and durations
4. Timer presets persist in SQLite database across server restarts
5. Completed timers are recorded in history table
6. UI is visually appealing with good color contrast and readability
7. Both frontend and backend start without errors
8. All validation commands pass successfully
9. HTML page title begins with "multiport-test-3-timer"
10. Application is accessible via public URL with proper CORS configuration

## Validation Commands

Execute these commands in order to validate the implementation:

```bash
# 1. Backend validation
cd /home/user/server
uv run pytest tests/ -v

# 2. Start backend server (background)
cd /home/user/server
uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 &

# 3. Test backend health
curl http://localhost:8000/health

# 4. Frontend build validation
cd /home/user/client
npm run build

# 5. Start frontend server (background)
cd /home/user/client
npm run dev -- --host 0.0.0.0 --port 5173 &

# 6. Full system validation
# - Frontend accessible at http://localhost:5173
# - Backend API accessible at http://localhost:8000
# - Create a preset via UI and verify in database
# - Run a timer to completion and verify history record

# 7. Database validation
cd /home/user/server
sqlite3 timer.db "SELECT * FROM timer_preset;"
sqlite3 timer.db "SELECT * FROM timer_history;"
```

## Notes

- Use `0.0.0.0` as host for both servers to ensure external accessibility in E2B sandbox
- Frontend must proxy API requests through Vite config to avoid CORS during development
- For production, ensure CORS origins include the E2B public URL format
- Timer logic runs client-side for responsiveness; backend only stores presets and history
- Consider adding sound notification when timer completes (optional enhancement)
- SQLite is suitable for this use case; no need for complex migration tools
- Database file will be created automatically on first run
- Visual design should prioritize readability with high contrast and large fonts for timer display
