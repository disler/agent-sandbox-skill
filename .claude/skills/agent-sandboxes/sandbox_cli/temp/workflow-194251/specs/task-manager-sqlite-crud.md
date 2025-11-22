# Plan: Task Manager with SQLite CRUD Operations

## Task Description
Build a full-stack Task Manager application with complete CRUD (Create, Read, Update, Delete) operations using:
- Frontend: Vite + Vue 3 + TypeScript + Pinia
- Backend: FastAPI + uvicorn + Python (uv)
- Database: SQLite

## Objective
Create a fully functional task management application where users can create, read, update, and delete tasks through a modern web interface. The application will have a clean separation between frontend (Vue), backend (FastAPI), and database (SQLite) layers, with a RESTful API connecting them.

## Problem Statement
Users need a simple, efficient way to manage their daily tasks with persistent storage. The application should provide an intuitive interface for task management while demonstrating proper full-stack architecture with separated concerns.

## Solution Approach
The application will follow a three-tier architecture:
1. **Frontend (Vue 3 + TypeScript)**: Modern, reactive UI with form inputs for task creation/editing and a responsive list for displaying tasks
2. **Backend (FastAPI)**: RESTful API with endpoints for all CRUD operations, request validation, and proper error handling
3. **Database (SQLite)**: Lightweight, file-based database with a tasks table storing title, description, status, and timestamps

**Request/Response Flow**:
- User interacts with Vue UI → Pinia store dispatches action → API client sends HTTP request → FastAPI endpoint validates → Database operation → JSON response → Pinia updates state → Vue reactively updates UI

## Relevant Files
Use these files and directories to complete the task:

### New Files
- `client/src/App.vue` - Main Vue application component with task list and form
- `client/src/stores/taskStore.ts` - Pinia store for task state management
- `client/src/services/api.ts` - API client for backend communication
- `client/src/types/task.ts` - TypeScript interfaces for task data
- `client/vite.config.ts` - Vite configuration with proxy for API calls
- `server/main.py` - FastAPI application with CRUD endpoints
- `server/models.py` - SQLAlchemy models for tasks
- `server/schemas.py` - Pydantic schemas for request/response validation
- `server/database.py` - Database connection and session management
- `server/crud.py` - CRUD operations for tasks
- `server/tasks.db` - SQLite database file (created automatically)

### Dependencies
- Frontend:
  - Already installed: `npm` (via Node.js 22), `vite@5.4.11`, `vue@3`, `pinia`, `typescript`
  - Add: `npm install axios` (for API calls)
- Backend:
  - Initialize: `cd server && uv init --app`
  - Add: `uv add fastapi uvicorn[standard] sqlalchemy pydantic python-multipart`
  - Dev dependencies: `uv add --dev pytest httpx`
- Database:
  - Add: `uv add aiosqlite` (async SQLite driver)
- Shared/Tooling:
  - Frontend linting: `npm install --save-dev eslint @typescript-eslint/parser @typescript-eslint/eslint-plugin`

## Implementation Phases

### Phase 1: Foundation
- Initialize backend project with uv
- Set up SQLite database with tasks table
- Configure FastAPI with CORS for frontend communication
- Initialize frontend with Vite proxy pointing to backend
- Verify both services start successfully (backend on 8000, frontend on 5173)

### Phase 2: Core Implementation
- Implement database models and CRUD functions
- Build FastAPI endpoints for all CRUD operations
- Create Pinia store with task management actions
- Build Vue components for task list and form
- Wire API client to connect frontend to backend

### Phase 3: Integration & Polish
- Test full request/response cycle for all operations
- Add loading states and error handling in UI
- Style components with clean, modern CSS
- Add input validation on both frontend and backend
- Test edge cases (empty lists, validation errors, database errors)

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### 1. Bootstrap & Verify Stack
- Create `server` directory and initialize FastAPI project with `uv init --app`
- Verify `client` directory exists with Vite + Vue 3 + TypeScript setup
- Install frontend dependencies: `cd client && npm install axios`
- Install backend dependencies: `cd server && uv add fastapi uvicorn[standard] sqlalchemy aiosqlite pydantic python-multipart`
- Test backend starts: `cd server && uv run uvicorn main:app --reload --port 8000`
- Test frontend starts: `cd client && npm run dev -- --host 0.0.0.0 --port 5173`

### 2. Backend & Database Foundation
- Create `server/database.py`: Set up SQLAlchemy engine with SQLite connection string `sqlite:///./tasks.db`
- Create `server/models.py`: Define Task model with columns: id (int, primary key), title (str, not null), description (str, nullable), status (str, default 'pending'), created_at (datetime, auto)
- Create `server/schemas.py`: Define Pydantic schemas for TaskCreate, TaskUpdate, and TaskResponse
- Create `server/crud.py`: Implement functions for create_task, get_tasks, get_task, update_task, delete_task
- Initialize database on startup in `server/main.py`

### 3. Backend API Implementation
- Create `server/main.py` with FastAPI app and CORS middleware
- Implement POST `/api/tasks` - Create new task
- Implement GET `/api/tasks` - List all tasks
- Implement GET `/api/tasks/{task_id}` - Get single task
- Implement PUT `/api/tasks/{task_id}` - Update task
- Implement DELETE `/api/tasks/{task_id}` - Delete task
- Add error handling for 404 (task not found) and 422 (validation errors)

### 4. Frontend Foundation
- Create `client/src/types/task.ts`: Define Task interface matching backend schema
- Create `client/src/services/api.ts`: Axios instance with base URL `/api` and functions for all CRUD operations
- Update `client/vite.config.ts`: Add proxy config to forward `/api` requests to `http://localhost:8000`
- Create `client/src/stores/taskStore.ts`: Pinia store with state (tasks array, loading, error) and actions for CRUD operations

### 5. Frontend UI Implementation
- Create `client/src/components/TaskForm.vue`: Form component with inputs for title, description, and status dropdown
- Create `client/src/components/TaskList.vue`: List component displaying tasks with edit and delete buttons
- Create `client/src/components/TaskItem.vue`: Individual task card with status badge
- Update `client/src/App.vue`: Main layout with TaskForm and TaskList, connect to Pinia store
- Add CSS styling for clean, modern look with proper spacing and colors

### 6. Integration & Error Handling
- Connect all frontend components to Pinia store actions
- Add loading spinners for async operations
- Display error messages for failed operations
- Add confirmation dialog for delete operations
- Handle empty state when no tasks exist
- Test all CRUD flows end-to-end

### 7. Testing & Verification
- Backend tests: Create `server/tests/test_api.py` with pytest for all endpoints
- Test database operations with in-memory SQLite for isolation
- Frontend manual testing: Create, read, update, delete tasks through UI
- Test validation: Try creating task with empty title, verify error handling
- Test edge cases: Delete non-existent task, update with invalid status
- Full integration test: Start both servers and perform complete user flow

## Testing Strategy
- Backend:
  - Unit tests for CRUD functions in `crud.py` with test database
  - Integration tests for FastAPI endpoints using TestClient
  - Test all HTTP methods and status codes (200, 201, 404, 422)
- Database:
  - Verify schema creation with SQLAlchemy metadata
  - Test constraints (not null, default values)
  - Verify timestamps auto-populate correctly
- Frontend:
  - Manual testing of all UI interactions
  - Component tests for TaskForm validation
  - Store tests for state management and API calls
- Combined:
  - End-to-end test: Start backend on 8000, frontend on 5173
  - Perform full CRUD cycle through UI and verify database state
  - Test CORS configuration and proxy setup

## Acceptance Criteria
- [ ] Backend API runs on port 8000 with all 5 CRUD endpoints functional
- [ ] Frontend UI runs on port 5173 and communicates with backend via proxy
- [ ] SQLite database persists tasks between server restarts
- [ ] Users can create tasks with title (required), description (optional), and status
- [ ] Users can view all tasks in a list with proper formatting
- [ ] Users can edit task details and status
- [ ] Users can delete tasks with confirmation
- [ ] All API responses return proper status codes and JSON
- [ ] Error messages display in UI for failed operations
- [ ] Loading states show during API calls
- [ ] UI is clean, modern, and responsive

## Validation Commands
Execute these commands to validate the task is complete:

```bash
# 1. Backend validation
cd server
uv run uvicorn main:app --reload --port 8000 &
sleep 3
curl http://localhost:8000/api/tasks  # Should return [] or list of tasks
uv run pytest  # Should pass all tests

# 2. Database validation
ls tasks.db  # Should exist
sqlite3 tasks.db "SELECT * FROM tasks;"  # Should show tasks table

# 3. Frontend validation
cd ../client
npm run build  # Should build successfully
npm run dev -- --host 0.0.0.0 --port 5173 &
sleep 5
curl http://localhost:5173  # Should return HTML

# 4. Full integration test
# With both servers running:
curl -X POST http://localhost:8000/api/tasks -H "Content-Type: application/json" -d '{"title":"Test Task","description":"Testing","status":"pending"}'
curl http://localhost:8000/api/tasks  # Should return the created task
# Open browser to http://localhost:5173 and verify UI shows the task
```

## Notes
- The fullstack-vue-fastapi-node22 template includes Node.js 22, uv, and all frontend dependencies pre-installed
- SQLite database file will be created automatically in the server directory on first run
- CORS must be configured to allow frontend (localhost:5173) to call backend (localhost:8000)
- Use async/await for all database operations with aiosqlite for better performance
- Pinia store should handle all API calls to keep components clean and reusable
- Status dropdown should only allow values: 'pending', 'in-progress', 'completed'
- Add proper TypeScript types throughout frontend code for better DX
- Consider adding a loading skeleton for better UX during initial data fetch
