# Plan: Easy Notes App

## Task Description
Build a simple, user-friendly notes application that allows users to create, read, update, and delete notes. The application will use:
- Frontend: Vite + Vue 3 + TypeScript + Pinia
- Backend: FastAPI + uvicorn + Python (uv)
- Database: SQLite

## Objective
Create a fully functional notes application with a clean, intuitive UI where users can manage their notes. The application will have a responsive Vue 3 frontend communicating with a FastAPI backend that persists notes in a SQLite database.

## Problem Statement
Users need a simple, fast way to capture and organize their thoughts and ideas. The application should provide an elegant interface for creating, viewing, editing, and deleting notes without unnecessary complexity.

## Solution Approach
The application will follow a clean three-tier architecture:
1. **Frontend (Vue 3)**: Single-page application with a notes list view and inline editing capabilities
2. **Backend (FastAPI)**: RESTful API providing CRUD endpoints for notes management with proper validation
3. **Database (SQLite)**: Simple relational database storing notes with id, title, content, and timestamps

Request/Response Flow:
- User creates/edits note → Frontend sends POST/PUT to `/api/notes` → Backend validates → Database persists → Response with note data → Frontend updates UI
- User views notes → Frontend sends GET to `/api/notes` → Backend queries database → Response with notes array → Frontend renders list
- User deletes note → Frontend sends DELETE to `/api/notes/{id}` → Backend removes from database → Frontend updates UI

## Relevant Files

### New Files

**Backend:**
- `/home/user/backend/main.py` - FastAPI application entry point with CORS and routes
- `/home/user/backend/models.py` - Pydantic models for request/response validation
- `/home/user/backend/database.py` - SQLite database connection and tables
- `/home/user/backend/crud.py` - Database operations (create, read, update, delete)
- `/home/user/backend/pyproject.toml` - Python dependencies managed by uv

**Frontend:**
- `/home/user/frontend/index.html` - HTML entry point with workflow ID in title
- `/home/user/frontend/src/main.ts` - Vue application initialization
- `/home/user/frontend/src/App.vue` - Main application component
- `/home/user/frontend/src/stores/notes.ts` - Pinia store for notes state management
- `/home/user/frontend/src/components/NotesList.vue` - Notes list display component
- `/home/user/frontend/src/components/NoteEditor.vue` - Note creation/editing component
- `/home/user/frontend/src/services/api.ts` - API client for backend communication
- `/home/user/frontend/vite.config.ts` - Vite configuration with proxy for backend API
- `/home/user/frontend/package.json` - Frontend dependencies

**Shared:**
- `/home/user/frontend/.env` - Frontend environment variables (API base URL)
- `/home/user/backend/.env` - Backend environment variables (if needed)

### Dependencies

**Frontend:**
```bash
npm create vite@latest frontend -- --template vue-ts
cd frontend
npm install pinia
npm install axios
npm install --save-dev @testing-library/vue vitest
```

**Backend:**
```bash
mkdir backend && cd backend
uv init --app
uv add fastapi uvicorn[standard] pydantic sqlalchemy aiosqlite
uv add --dev pytest httpx
```

**Shared/Tooling:**
```bash
npm install --save-dev eslint prettier
```

## Implementation Phases

### Phase 1: Foundation
- Scaffold frontend and backend projects with proper directory structure
- Initialize SQLite database with notes table schema
- Configure CORS for cross-origin requests
- Run both services to confirm they start successfully
- Set up environment variables for API communication

### Phase 2: Core Implementation
- Implement FastAPI CRUD endpoints for notes (`GET /api/notes`, `POST /api/notes`, `PUT /api/notes/{id}`, `DELETE /api/notes/{id}`)
- Create SQLite schema with migration for notes table (id, title, content, created_at, updated_at)
- Build Vue 3 components for notes list and editor
- Implement Pinia store for state management
- Create API service layer for HTTP communication

### Phase 3: Integration & Polish
- Connect frontend to backend API with proper error handling
- Add loading states and user feedback (toasts/notifications)
- Implement responsive design with appealing color scheme (avoid poor contrast)
- Add input validation on both frontend and backend
- Polish UI/UX with smooth transitions and intuitive interactions

## Step by Step Tasks

### 1. Bootstrap & Verify Stack
- Create `/home/user/backend` directory and initialize FastAPI project with uv
- Create `/home/user/frontend` directory and initialize Vite + Vue 3 + TypeScript project
- Install backend dependencies: `uv add fastapi uvicorn[standard] pydantic sqlalchemy aiosqlite`
- Install frontend dependencies: `npm install pinia axios`
- Configure Vite to proxy API requests to backend (port 8000)
- Start backend server: `uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000`
- Start frontend server: `npm run dev -- --host 0.0.0.0 --port 5173`
- Verify both servers start without errors

### 2. Backend & Database Foundation
- Create SQLite database schema in `database.py`:
  - notes table: id (INTEGER PRIMARY KEY), title (TEXT NOT NULL), content (TEXT), created_at (TIMESTAMP), updated_at (TIMESTAMP)
- Implement database initialization and connection management
- Create Pydantic models in `models.py`:
  - `NoteBase`: title, content
  - `NoteCreate`: inherits from NoteBase
  - `NoteUpdate`: inherits from NoteBase with optional fields
  - `Note`: inherits from NoteBase with id, created_at, updated_at
- Set up database session dependency for FastAPI routes

### 3. Backend API Implementation
- Implement CRUD operations in `crud.py`:
  - `get_notes()`: retrieve all notes ordered by updated_at desc
  - `get_note(note_id)`: retrieve single note by id
  - `create_note(note_data)`: create new note with timestamps
  - `update_note(note_id, note_data)`: update existing note and timestamp
  - `delete_note(note_id)`: delete note by id
- Create FastAPI routes in `main.py`:
  - `GET /api/notes`: list all notes
  - `GET /api/notes/{id}`: get single note
  - `POST /api/notes`: create new note
  - `PUT /api/notes/{id}`: update note
  - `DELETE /api/notes/{id}`: delete note
  - `GET /api/health`: health check endpoint
- Configure CORS to allow requests from frontend origin
- Add proper error handling and HTTP status codes (404 for not found, 422 for validation errors)

### 4. Frontend Foundation
- Update `index.html` to include workflow ID in title: `<title>test-workflow-browser-validation - Notes App</title>`
- Configure Vite in `vite.config.ts` to proxy `/api` requests to `http://localhost:8000`
- Create API service in `services/api.ts`:
  - Base axios instance with `/api` prefix
  - `fetchNotes()`: GET /notes
  - `createNote(data)`: POST /notes
  - `updateNote(id, data)`: PUT /notes/{id}
  - `deleteNote(id)`: DELETE /notes/{id}
- Create Pinia store in `stores/notes.ts`:
  - State: notes array, loading boolean, error string
  - Actions: loadNotes, addNote, editNote, removeNote
  - Integrate with API service

### 5. Frontend UI Components
- Create `NotesList.vue` component:
  - Display notes in a grid or list layout
  - Show title, content preview (first 100 chars), and timestamp
  - Include edit and delete buttons for each note
  - Handle empty state when no notes exist
  - Use appealing color scheme with good contrast (e.g., soft blues and whites, dark text on light backgrounds)
- Create `NoteEditor.vue` component:
  - Form with title input and content textarea
  - Submit button to save note
  - Cancel button to clear form
  - Validation for required title field
  - Display inline errors
- Update `App.vue`:
  - Compose NotesList and NoteEditor components
  - Add header with app title
  - Include "Add Note" button/toggle
  - Implement responsive layout (mobile-friendly)
  - Add loading spinner during API calls
  - Display error messages from store

### 6. Integration & State Management
- Wire up Pinia store actions to API calls with proper error handling
- Implement optimistic UI updates for instant feedback
- Add loading states for all async operations
- Handle API errors gracefully with user-friendly messages
- Add success notifications for create/update/delete operations
- Implement auto-refresh after mutations

### 7. Testing & Verification

**Database Testing:**
- Verify database file creation: `/home/user/backend/notes.db`
- Test schema creation with sample data insertion
- Validate timestamp auto-generation on create/update

**Backend Testing:**
- Unit tests for CRUD operations in `crud.py`
- Integration tests for API endpoints with test database
- Test validation errors (empty title, invalid ID)
- Test CORS headers in responses
- Run: `uv run pytest tests/`

**Frontend Testing:**
- Component unit tests for NotesList and NoteEditor
- Test Pinia store actions and state mutations
- Test API service error handling
- Run: `npm run test`

**Full-System Testing:**
- Start both backend and frontend servers
- Create a new note via UI and verify it appears in list
- Edit an existing note and verify changes persist
- Delete a note and verify it's removed
- Test error handling (network errors, validation failures)
- Verify responsive design on mobile viewport
- Check browser console for errors
- Validate CORS works correctly
- Commands:
  ```bash
  # Terminal 1: Start backend
  cd /home/user/backend && uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000

  # Terminal 2: Start frontend
  cd /home/user/frontend && npm run dev -- --host 0.0.0.0 --port 5173

  # Terminal 3: Test endpoints
  curl http://localhost:8000/api/health
  curl http://localhost:8000/api/notes
  ```

## Testing Strategy

**Backend:**
- Unit tests for database operations (create, read, update, delete notes)
- Integration tests for FastAPI routes with test SQLite database
- Validation tests for Pydantic models (missing required fields, invalid data types)
- CORS tests to ensure proper headers

**Database:**
- Schema creation and migration tests
- Data integrity tests (foreign keys, constraints)
- Timestamp auto-generation tests
- Rollback/forward migration tests (if using Alembic)

**Frontend:**
- Component unit tests for NotesList and NoteEditor
- Pinia store tests for state mutations and actions
- API service tests with mocked responses
- Visual tests for layout and styling

**Combined:**
- End-to-end tests starting both backend and frontend
- Smoke tests for primary user flows:
  1. Load app → See empty state or existing notes
  2. Create note → Verify appears in list
  3. Edit note → Verify changes persist
  4. Delete note → Verify removal
- Commands to launch and test:
  ```bash
  # Start full stack
  cd /home/user/backend && uv run uvicorn main:app --host 0.0.0.0 --port 8000 &
  cd /home/user/frontend && npm run dev -- --host 0.0.0.0 --port 5173 &

  # Verify health
  curl http://localhost:8000/api/health
  curl http://localhost:5173
  ```

## Acceptance Criteria

1. ✅ Backend API running on port 8000 with health endpoint responding
2. ✅ Frontend application running on port 5173 and accessible via browser
3. ✅ SQLite database created with notes table schema
4. ✅ Users can create a new note with title and content
5. ✅ Users can view all notes in a list/grid layout
6. ✅ Users can edit existing notes and see changes persist
7. ✅ Users can delete notes and see them removed from the list
8. ✅ CORS configured correctly for cross-origin requests
9. ✅ Frontend has appealing, high-contrast color scheme
10. ✅ HTML page title includes workflow ID: "test-workflow-browser-validation"
11. ✅ Loading states shown during API operations
12. ✅ Error messages displayed for failed operations
13. ✅ Responsive design works on mobile and desktop viewports
14. ✅ All backend tests passing
15. ✅ All frontend tests passing
16. ✅ End-to-end user flow validated

## Validation Commands

Execute these commands to validate the task is complete:

**Backend Validation:**
```bash
cd /home/user/backend
uv run uvicorn main:app --host 0.0.0.0 --port 8000 &
sleep 3
curl http://localhost:8000/api/health
curl http://localhost:8000/api/notes
uv run pytest tests/
```

**Database Validation:**
```bash
cd /home/user/backend
ls -la notes.db
sqlite3 notes.db "SELECT name FROM sqlite_master WHERE type='table';"
sqlite3 notes.db "SELECT * FROM notes LIMIT 5;"
```

**Frontend Validation:**
```bash
cd /home/user/frontend
npm run build
npm run test
npm run dev -- --host 0.0.0.0 --port 5173 &
sleep 3
curl http://localhost:5173
```

**Full-Stack Integration:**
```bash
# Start backend
cd /home/user/backend && uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Start frontend
cd /home/user/frontend && npm run dev -- --host 0.0.0.0 --port 5173 &
FRONTEND_PID=$!

# Wait for startup
sleep 5

# Test health
curl http://localhost:8000/api/health

# Test CRUD flow
curl -X POST http://localhost:8000/api/notes \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Note","content":"This is a test"}'

curl http://localhost:8000/api/notes

# Test frontend loads
curl http://localhost:5173 | grep "test-workflow-browser-validation"

# Cleanup
kill $BACKEND_PID $FRONTEND_PID
```

## Notes

**Technology Choices:**
- **Vite**: Fast build tool with HMR for development
- **Vue 3**: Modern reactive framework with Composition API
- **Pinia**: Official state management for Vue 3 (replaces Vuex)
- **FastAPI**: High-performance async Python web framework
- **SQLite**: Lightweight, serverless database perfect for this use case
- **uv**: Fast Python package installer and environment manager

**Design Considerations:**
- Keep UI simple and focused on core functionality
- Use soft, professional colors (avoid harsh contrasts)
- Ensure text is always readable (dark on light or light on dark with sufficient contrast)
- Mobile-first responsive design
- Optimistic UI updates for better perceived performance
- Graceful error handling with user-friendly messages

**Development Notes:**
- Backend runs on port 8000 by default
- Frontend proxies `/api` requests to backend via Vite config
- Frontend runs on port 5173 (Vite default)
- Both services must bind to `0.0.0.0` to be accessible from outside sandbox
- CORS must allow frontend origin for API access
- HTML title must start with workflow ID: "test-workflow-browser-validation"

**Deployment Considerations:**
- In production, frontend would be built and served as static files
- Backend would run behind a reverse proxy (nginx, caddy)
- Database would likely migrate to PostgreSQL for multi-user scenarios
- For E2B sandbox, we're exposing frontend on port 5173 with backend accessible via proxy
