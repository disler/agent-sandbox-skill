# Plan: Simple Notes App

## Task Description
Build a full-stack note-taking app where users can create, edit, delete, and search notes using a clean, responsive UI. Stack: frontend = vite vue-ts pinia, backend = astral uv python fast api, database = sqlite.

## Objective
Deliver a running app with a FastAPI + SQLite backend and Vite + Vue 3 + Pinia frontend. Users can manage notes (title + body, updated timestamp) with live list/search, and state persists in the database.

## Problem Statement
Users need a lightweight notes UI with fast CRUD and search; the system must persist data safely and expose a clear API for the frontend.

## Solution Approach
Structure `/home/user/app` with separate `backend` and `frontend` projects. Backend: FastAPI with SQLModel + SQLite for CRUD/search, CORS open to the Vite host, and simple seed. Frontend: Vue 3 + Pinia + axios, with a sidebar list/search and main editor pane. Use a shared API client, types, and loading/error states. Provide validation via pytest (backend) and Vitest (frontend build smoke).

## Relevant Files
Use these files and directories to complete the task (frontend and backend remain separated):
- `/home/user/app/backend/app/main.py` – FastAPI app entry, CORS, router include.
- `/home/user/app/backend/app/db.py` – SQLite engine/session, init helper.
- `/home/user/app/backend/app/models.py` – SQLModel Note definition + CRUD utilities.
- `/home/user/app/backend/app/schemas.py` – Pydantic models for requests/responses.
- `/home/user/app/backend/app/api/notes.py` – Router with CRUD/search endpoints.
- `/home/user/app/backend/tests/test_notes.py` – Core backend tests.
- `/home/user/app/frontend/index.html` – Set document title (prefix with WORKFLOW_ID).
- `/home/user/app/frontend/src/main.ts` – Vue bootstrap, Pinia, router.
- `/home/user/app/frontend/src/App.vue` – Layout shell (sidebar + editor).
- `/home/user/app/frontend/src/views/NotesView.vue` – Notes page wiring store + UI.
- `/home/user/app/frontend/src/stores/notes.ts` – Pinia store with API calls.
- `/home/user/app/frontend/src/api/client.ts` – axios instance with base URL/env.
- `/home/user/app/frontend/src/components/NoteList.vue` and `NoteEditor.vue` – UI components for list/search and editor form.
- `.env` – copy to sandbox if API keys are ever needed: `cp .env .claude/skills/agent-sandboxes/sandbox_cli/temp/codex-cli-codex-5-1-max-high--easy_notes_app/.env` (not required for this task).

### New Files
- Backend: `app/main.py`, `app/db.py`, `app/models.py`, `app/schemas.py`, `app/api/notes.py`, `tests/test_notes.py`
- Frontend: `src/api/client.ts`, `src/stores/notes.ts`, `src/views/NotesView.vue`, `src/components/NoteList.vue`, `src/components/NoteEditor.vue`, `src/styles/base.css`
- Config updates: `frontend/index.html`, `frontend/vite.config.ts`

### Dependencies
- Frontend: `npm create vite@latest frontend -- --template vue-ts`, `cd frontend && npm install axios pinia vue-router @vueuse/core`, dev: `npm install -D @types/node @vitejs/plugin-vue vitest jsdom @vue/test-utils @testing-library/vue`
- Backend: `uv init --app backend`, `cd backend && uv add fastapi uvicorn[standard] sqlmodel aiosqlite python-multipart`, dev: `uv add --dev pytest pytest-asyncio httpx`
- Database: SQLite (built-in), managed via SQLModel.
- Shared/Tooling: Use Vite dev server on 5173 with proxy to FastAPI 8000; uv for backend env.

## Implementation Phases
### Phase 1: Foundation
- Create `/home/user/app` with `backend/` and `frontend/` projects; run initial install commands.
- Configure Vite dev server host/port and FastAPI app skeleton; run each server once to confirm startup.

### Phase 2: Core Implementation
- Implement SQLite models, CRUD, and routers; wire DB init on startup.
- Build Vue layout shell, API client, Pinia store, and base components for list/editor.

### Phase 3: Integration & Polish
- Connect frontend to live backend, add loading/error states, search filter, and responsive styling.
- Add tests/build steps and ensure WORKFLOW_ID-prefixed title; prepare host readiness.

## Step by Step Tasks
### 1. Bootstrap & Verify Stack
- Create `/home/user/app` with `backend` and `frontend` directories.
- Backend: `cd backend && uv init --app .` then add deps; verify `uv run uvicorn app.main:app --reload` boots after stubbing.
- Frontend: `npm create vite@latest frontend -- --template vue-ts`; install deps; adjust `vite.config.ts` for host `0.0.0.0`, port `5173`, and proxy `/api` -> `http://localhost:8000`. Run `npm run dev -- --host --port 5173` once to verify scaffold.

### 2. Backend & Database Foundation
- Add `app/db.py` with SQLModel engine/session helpers pointing to `/home/user/app/backend/app/notes.db`.
- Define `app/models.py` SQLModel `Note` with id, title, body, updated_at; include CRUD helpers (list with search, get, create, update, delete).
- Add `app/schemas.py` for create/update/read models (pydantic).
- Build `app/api/notes.py` router with CRUD/search endpoints (`/api/notes`, `/api/notes/{id}`) using dependencies.
- In `app/main.py`, create FastAPI app, include router, enable CORS for `*` and Vite host, and initialize DB tables on startup.

### 3. Frontend Foundation
- Update `frontend/index.html` title to begin with `codex-cli-codex-5-1-max-high--easy_notes_app` and include a purposeful Google Font; add `src/styles/base.css` for layout/theme tokens.
- In `src/main.ts`, install Pinia, router (single Notes view), and global styles.
- Create `src/api/client.ts` with axios base URL from `VITE_API_BASE_URL` (fallback `http://localhost:8000`).
- Create Pinia store `src/stores/notes.ts` with state (notes list, activeNoteId, loading/error), getters (sorted/filtered by search), and actions calling backend via axios.

### 4. Feature Implementation
- Build `NoteList.vue` for sidebar (search input, new note button, list with preview + selection, empty state).
- Build `NoteEditor.vue` for title/body inputs, save/delete buttons, loading indicators, and optimistic UI refresh.
- Build `NotesView.vue` to compose list + editor, manage routing state (if using router) or local selection, and call store actions on mount (fetch notes).
- Ensure graceful handling when no note selected and when API errors occur (toasts/message state).

### 5. Integration & Observability
- Wire store actions to backend endpoints; ensure search query param is used for filtering server-side.
- Ensure FastAPI uses `0.0.0.0` host, port `8000`; Vite dev server uses `0.0.0.0:5173` with proxy for `/api`.
- Add simple logging on backend requests and HTTP error handling in axios (interceptor).
- Keep styles responsive (flex layout, collapsible sidebar on small screens).

### 6. Testing & Verification
- Backend: add `pytest` test covering create/list/update/delete round trip using TestClient and temp DB.
- Frontend: run `npm run build` and a vitest smoke test for Pinia store behavior.
- Full stack: start backend `uv run uvicorn app.main:app --host 0.0.0.0 --port 8000` and frontend `npm run dev -- --host --port 5173`, then curl `/api/notes` and load UI to verify flows.

## Testing Strategy
- Backend: pytest with FastAPI TestClient hitting CRUD endpoints against an in-memory/temp SQLite database; ensure search filter works and timestamps update.
- Database: verify table creation and unique IDs; no separate migrations needed for SQLite.
- Frontend: vitest for store logic (creation/update/delete) with mocked axios; build step ensures bundling correctness.
- Combined: manual/curl E2E—create note → list shows it → update → delete → list empty; verify via public URL once hosted.

## Acceptance Criteria
- Backend serves `/api/notes` CRUD with search query param, returns JSON with id/title/body/updated_at, and persists to SQLite.
- CORS allows the Vite origin; backend binds to `0.0.0.0:8000`.
- Frontend renders sidebar list + search + new note button and editor pane; notes load, can be created/edited/deleted, and search filters list.
- Title in `frontend/index.html` starts with `codex-cli-codex-5-1-max-high--easy_notes_app`.
- Tests/build commands succeed.

## Validation Commands
- Backend: `cd /home/user/app/backend && uv run pytest` and `uv run uvicorn app.main:app --host 0.0.0.0 --port 8000` (for manual smoke)
- Database: `cd /home/user/app/backend && uv run python -c "from app.db import create_db_and_tables; create_db_and_tables(); print('ok')"`
- Frontend: `cd /home/user/app/frontend && npm run build && npm run test`
- Full stack smoke: start backend (background), start frontend dev `npm run dev -- --host --port 5173`, then curl `http://localhost:8000/api/notes` and hit `http://localhost:5173`

## Notes
- Keep API base configurable via `VITE_API_BASE_URL` for hosted environment; Vite proxy handles local dev.
- Use consistent timestamp formatting (`datetime.isoformat()` from backend).
- Search should be case-insensitive on title, and list sorted by updated_at desc for recency.
