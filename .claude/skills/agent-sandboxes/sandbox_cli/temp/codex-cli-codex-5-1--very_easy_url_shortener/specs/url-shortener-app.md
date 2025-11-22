# Plan: URL Shortener Application

## Task Description
Build a minimal URL shortener application with a clean, professional UI. Users can paste long URLs, get short codes, and redirect via short codes. The application tracks click counts for analytics.

**Technology Stack:**
- Frontend: Vite + Vue 3 + TypeScript + Pinia
- Backend: FastAPI + uvicorn + Python (uv)
- Database: SQLite

## Objective
Create a fully functional URL shortener with a Vue 3 frontend and FastAPI backend that:
- Accepts long URLs and generates unique 6-character short codes
- Redirects users from short codes to original URLs
- Tracks and displays click statistics
- Provides a clean, professional, and functional UI

## Relevant Files

### New Files
- `/home/user/frontend/` - Vue 3 application root
- `/home/user/frontend/src/main.ts` - Application entry point
- `/home/user/frontend/src/App.vue` - Root component
- `/home/user/frontend/src/components/UrlShortener.vue` - Main URL shortener component
- `/home/user/frontend/src/stores/urlStore.ts` - Pinia store for URL state management
- `/home/user/frontend/vite.config.ts` - Vite configuration with proxy
- `/home/user/backend/` - FastAPI application root
- `/home/user/backend/src/main.py` - FastAPI application entry point
- `/home/user/backend/src/database.py` - Database connection and models
- `/home/user/backend/src/routes.py` - API route definitions
- `/home/user/backend/src/services.py` - Business logic for URL shortening
- `/home/user/backend/data/urls.db` - SQLite database file
- `/home/user/backend/.env` - Environment configuration

### Dependencies
- Frontend:
  - `npm create vite@latest frontend -- --template vue-ts`
  - `npm install pinia`
  - `npm install --save-dev @vitejs/plugin-vue`
- Backend:
  - `uv init --app backend`
  - `uv add fastapi uvicorn[standard] pydantic sqlalchemy aiosqlite python-dotenv`
  - `uv add --dev pytest httpx`
- Database:
  - SQLite (included with Python)
  - `uv add sqlalchemy aiosqlite`

## Step by Step Tasks

### 1. Bootstrap & Verify Stack
- Create `/home/user/frontend` directory and initialize Vite + Vue 3 + TypeScript project
- Create `/home/user/backend` directory and initialize uv Python project
- Install all dependencies for frontend (Vite, Vue, Pinia, TypeScript)
- Install all dependencies for backend (FastAPI, uvicorn, SQLAlchemy, aiosqlite)
- Configure CORS in backend to allow frontend requests
- Run both frontend and backend dev servers to confirm they boot
- Frontend should run on port 5173, backend on port 8000

### 2. Backend & Database Foundation
- Create SQLite database schema with `urls` table:
  - `id` (INTEGER PRIMARY KEY AUTOINCREMENT)
  - `long_url` (TEXT NOT NULL)
  - `short_code` (TEXT UNIQUE NOT NULL)
  - `clicks` (INTEGER DEFAULT 0)
  - `created_at` (DATETIME DEFAULT CURRENT_TIMESTAMP)
- Set up SQLAlchemy models and async engine for SQLite
- Implement database initialization and table creation on startup
- Add database dependency injection for FastAPI routes

### 3. Backend API Implementation
- **POST /api/shorten**: Accept long URL, generate random 6-character short code, store in database, return short code
  - Validate URL format
  - Check for uniqueness of short code (regenerate if collision)
  - Return JSON with `short_code`, `long_url`, and creation timestamp
- **GET /:code**: Retrieve long URL by short code, increment clicks, return 302 redirect
  - Return 404 if short code not found
  - Atomically increment click counter
- **GET /api/stats/:code**: Return click statistics for a short code
  - Return JSON with `short_code`, `long_url`, `clicks`, `created_at`
  - Return 404 if short code not found
- Add health check endpoint: **GET /health**

### 4. Frontend Foundation
- Configure Vite to proxy `/api/*` requests to `http://localhost:8000`
- Create Pinia store for managing URL state (shortened URLs, stats)
- Set up TypeScript interfaces for API responses
- Configure Vue Router (optional for multi-page if needed, or keep single-page)

### 5. Frontend UI Implementation
- Create main `UrlShortener.vue` component with:
  - Input field for long URL with placeholder
  - Submit button to shorten URL
  - Display area for shortened URL (with copy button)
  - Display area for click count
  - Clean, professional styling with good contrast (avoid hard-to-read color combinations)
  - Loading states during API calls
  - Error handling and user feedback
- Style the UI with modern CSS (flexbox/grid, clean typography, pleasant colors)
- Make shortened URL clickable and copyable
- Auto-fetch stats after shortening a URL

### 6. Integration & CORS Configuration
- Configure FastAPI CORS middleware to allow frontend origin (`http://localhost:5173`)
- Test frontend calling backend API from browser
- Handle loading and error states in Vue components
- Add proper error messages for failed requests

### 7. Testing & Verification
- **Backend Tests**:
  - Test `POST /api/shorten` creates new short codes
  - Test `POST /api/shorten` handles duplicate URLs gracefully
  - Test `GET /:code` redirects correctly and increments clicks
  - Test `GET /api/stats/:code` returns correct statistics
  - Test 404 responses for invalid short codes
  - Verify database schema and data persistence
- **Frontend Tests**:
  - Test URL input validation
  - Test API integration with mocked responses
  - Test copy-to-clipboard functionality
  - Verify UI updates after shortening URL
- **Full-Stack Integration**:
  - Start backend: `cd /home/user/backend && uv run uvicorn src.main:app --host 0.0.0.0 --port 8000`
  - Start frontend: `cd /home/user/frontend && npm run dev -- --host 0.0.0.0 --port 5173`
  - Test complete user flow: paste URL, get short code, visit short code, verify redirect, check stats
  - Verify click counter increments on each redirect

## Testing Strategy
- **Backend**: Unit tests for service functions (short code generation, URL validation), integration tests for FastAPI endpoints with test database
- **Database**: Verify schema creation, test unique constraints on short codes, validate click increment logic
- **Frontend**: Component tests for UrlShortener component, integration tests with mocked API responses
- **End-to-End**: Start both services, shorten a URL via UI, copy and visit the short link, verify redirect works, check stats endpoint shows correct click count

## Acceptance Criteria
- ✅ Backend API running on port 8000 with all endpoints functional
- ✅ Frontend UI running on port 5173 with clean, professional design
- ✅ Database properly initialized with urls table
- ✅ User can paste a long URL and receive a 6-character short code
- ✅ Short codes are unique and generate new ones on collision
- ✅ Visiting `/:code` redirects to the original long URL
- ✅ Click counter increments on each redirect
- ✅ Stats endpoint returns accurate click counts
- ✅ UI displays shortened URL in a copyable format
- ✅ UI shows click count for shortened URLs
- ✅ No color contrast issues making text hard to read
- ✅ All validation commands pass

## Validation Commands

Execute these commands to validate the implementation:

**Backend Validation:**
```bash
cd /home/user/backend
uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 &
sleep 3
curl http://localhost:8000/health
curl -X POST http://localhost:8000/api/shorten -H "Content-Type: application/json" -d '{"url":"https://example.com/very/long/url"}'
```

**Database Validation:**
```bash
cd /home/user/backend
uv run python -c "from src.database import engine, Base; import asyncio; asyncio.run(Base.metadata.create_all(engine))"
sqlite3 data/urls.db "SELECT * FROM urls;"
```

**Frontend Validation:**
```bash
cd /home/user/frontend
npm run build
npm run dev -- --host 0.0.0.0 --port 5173 &
sleep 5
curl http://localhost:5173
```

**Full-Stack Validation:**
```bash
# Start backend
cd /home/user/backend && uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 &

# Start frontend
cd /home/user/frontend && npm run dev -- --host 0.0.0.0 --port 5173 &

# Wait for services to start
sleep 5

# Test API flow
curl -X POST http://localhost:8000/api/shorten -H "Content-Type: application/json" -d '{"url":"https://anthropic.com"}'
# Note the short_code from response, then test redirect and stats
curl -I http://localhost:8000/abc123  # Replace abc123 with actual short_code
curl http://localhost:8000/api/stats/abc123  # Replace abc123 with actual short_code
```

## Notes
- Short code generation should use random alphanumeric characters (a-z, A-Z, 0-9) for a 6-character code
- CORS must be configured to allow `http://localhost:5173` origin
- Frontend should update the page title to begin with the workflow ID: `codex-cli-codex-5-1--very_easy_url_shortener`
- Use `0.0.0.0` as host for both services to ensure they're accessible from outside the sandbox
- Database file should be in `/home/user/backend/data/urls.db` directory
- Consider adding debouncing to the submit button to prevent double-clicks
- Shortened URLs should be displayed with the full redirect URL (e.g., `http://localhost:8000/abc123`)
- The UI should be responsive and work well on different screen sizes
