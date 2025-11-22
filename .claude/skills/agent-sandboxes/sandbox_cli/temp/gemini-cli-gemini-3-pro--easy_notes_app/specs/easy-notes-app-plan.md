# Plan: Simple Notes App

## Task Description
Build a full-stack Note Taking application allowing users to create, edit, delete, and search notes.
- **Frontend**: Vite + Vue 3 + TypeScript + Pinia
- **Backend**: FastAPI + uvicorn + Python (uv)
- **Database**: SQLite

## Objective
Deliver a fully functional notes application running in the sandbox with separate frontend and backend services, utilizing a persistent SQLite database.

## Relevant Files
- `frontend/`: Vue 3 application source
- `backend/`: FastAPI application source
- `backend/main.py`: Entry point for backend
- `backend/database.py`: Database connection and session management
- `backend/models.py`: SQLAlchemy models
- `backend/schemas.py`: Pydantic schemas for API
- `backend/crud.py`: CRUD operations
- `backend/routers/notes.py`: API routes for notes
- `frontend/src/stores/notes.ts`: Pinia store for notes state
- `frontend/src/components/NoteList.vue`: Sidebar component
- `frontend/src/components/NoteEditor.vue`: Main editor component
- `frontend/src/App.vue`: Main layout
- `frontend/src/services/api.ts`: Axios instance and API calls

### Dependencies
- **Frontend**: `npm create vite@latest`, `axios`, `pinia`, `vue-router`
- **Backend**: `uv init`, `fastapi`, `uvicorn[standard]`, `pydantic`, `sqlalchemy`, `aiosqlite` (for async if needed, or just standard sqlite driver)
- **Tooling**: `pytest`, `httpx` (for testing)

## Step by Step Tasks

### 1. Bootstrap & Verify Stack
- Initialize backend project with `uv init backend` and add dependencies (`fastapi`, `uvicorn`, `sqlalchemy`).
- Initialize frontend project with `npm create vite@latest frontend -- --template vue-ts` and install dependencies (`axios`, `pinia`).
- Verify both can start (Backend on 8000, Frontend on 5173).

### 2. Backend & Database Foundation
- Create `backend/database.py` to setup SQLite engine and SessionLocal.
- Define `Note` model in `backend/models.py` (id, title, content, updated_at).
- Create `backend/schemas.py` for Pydantic models (NoteCreate, NoteUpdate, NoteResponse).
- Implement `init_db` function to create tables.

### 3. Backend API Implementation
- Implement CRUD functions in `backend/crud.py`.
- Create `backend/routers/notes.py` with endpoints:
    - `GET /api/notes`: List all (id, title, preview).
    - `GET /api/notes/{id}`: Get full note.
    - `POST /api/notes`: Create note.
    - `PUT /api/notes/{id}`: Update note.
    - `DELETE /api/notes/{id}`: Delete note.
- specific handling for CORS in `backend/main.py`.

### 4. Frontend Foundation
- Setup Pinia in `frontend/src/main.ts`.
- Create `frontend/src/services/api.ts` configured to point to backend URL (handling dev/prod).
- Create `frontend/src/stores/notes.ts` to handle fetching, selecting, and saving notes.

### 5. Frontend Feature Implementation
- **Layout**: Create a 2-column layout in `App.vue`.
- **Note List**: Implement `NoteList.vue` with search bar and list of notes (highlight selected).
- **Editor**: Implement `NoteEditor.vue` with title input and textarea body. Auto-save or Save button.
- **Interactions**:
    - Clicking a note in list selects it.
    - "New Note" button clears selection and prepares editor.
    - "Delete" button removes note and clears selection.

### 6. Integration & Polish
- Ensure Frontend communicates correctly with Backend (CORS, proxy).
- Add loading states and basic error handling (e.g., if fetch fails).
- Style using CSS (flexbox/grid) for a clean, modern look.

### 7. Testing & Verification
- **Backend Test**: Write `tests/test_notes.py` using `pytest` and `httpx` to verify API endpoints.
- **Integration Test**: Run backend and frontend, verify "New Note" appears in list after creation.

## Acceptance Criteria
- Backend serves API at port 8000.
- Frontend serves UI at port 5173.
- User can create a note, see it in the list.
- User can edit a note, save, and updates persist.
- User can delete a note.
- Search functionality filters the note list.

## Validation Commands
- Backend: `cd backend && uv run uvicorn main:app --reload`
- Frontend: `cd frontend && npm run dev`
- Tests: `cd backend && uv run pytest`
