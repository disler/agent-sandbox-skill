# Plan: Todo List - Simple Task Manager

## Task Description
Build a single-user todo list application with add, complete, and delete functionality. No authentication required, just basic CRUD operations for todo items. The application will use a full-stack architecture with:
- Frontend: Vite + Vue 3 + TypeScript + Pinia (state management)
- Backend: FastAPI + uvicorn + Python (uv package manager)
- Database: SQLite (persistent storage)

## Objective
Create a fully functional, production-ready todo list application where users can:
1. Add new todos with text descriptions
2. Mark todos as complete/incomplete via checkboxes
3. Delete individual todos or clear all completed todos
4. Filter todos by status (All/Active/Completed)
5. View a count of remaining active todos
6. Have data persist across browser refreshes

## Problem Statement
Users need a simple, fast, and reliable way to manage their daily tasks without the overhead of authentication or complex features. The application must provide instant feedback, persist data reliably, and work seamlessly across devices.

## Solution Approach
The application follows a standard three-tier architecture:

1. **Frontend (Vue 3 + Pinia)**: Modern reactive UI with component-based architecture
   - Single-page application with client-side routing
   - Pinia store for centralized state management
   - Axios for HTTP client communication
   - Professional UI with modern design patterns

2. **Backend (FastAPI)**: RESTful API for business logic and data persistence
   - CRUD endpoints for todo operations
   - CORS configuration for frontend communication
   - Input validation with Pydantic models
   - Async/await for optimal performance

3. **Database (SQLite)**: Lightweight, file-based persistence
   - Simple schema with todos table
   - Auto-incrementing IDs
   - Timestamp tracking for created/updated times

**Data Flow**:
- User interacts with Vue components
- Components dispatch actions to Pinia store
- Store makes API calls via Axios to FastAPI backend
- Backend validates requests and queries SQLite database
- Response flows back through the stack to update UI

## Relevant Files

### Backend Structure
- `/home/user/backend/` - Root backend directory
- `/home/user/backend/src/` - Application source code
- `/home/user/backend/src/main.py` - FastAPI application entry point
- `/home/user/backend/src/models.py` - Pydantic models for request/response validation
- `/home/user/backend/src/database.py` - Database connection and ORM setup
- `/home/user/backend/src/crud.py` - Database CRUD operations
- `/home/user/backend/pyproject.toml` - Python dependencies (uv managed)
- `/home/user/backend/todos.db` - SQLite database file

### Frontend Structure
- `/home/user/frontend/` - Root frontend directory
- `/home/user/frontend/src/` - Vue application source
- `/home/user/frontend/src/main.ts` - Application entry point
- `/home/user/frontend/src/App.vue` - Root component
- `/home/user/frontend/src/components/TodoList.vue` - Main todo list component
- `/home/user/frontend/src/components/TodoItem.vue` - Individual todo item component
- `/home/user/frontend/src/components/TodoInput.vue` - Input form for new todos
- `/home/user/frontend/src/stores/todoStore.ts` - Pinia store for state management
- `/home/user/frontend/src/services/api.ts` - API client using Axios
- `/home/user/frontend/package.json` - NPM dependencies
- `/home/user/frontend/vite.config.ts` - Vite configuration
- `/home/user/frontend/index.html` - HTML entry point

### Shared/Configuration
- `/home/user/frontend/.env` - Frontend environment variables (API base URL)
- `/home/user/backend/.env` - Backend environment variables (if needed for API keys)

### New Files
All files listed above will be created as part of this implementation.

### Dependencies

#### Frontend
```bash
# Initialize Vite project with Vue + TypeScript
npm create vite@latest frontend -- --template vue-ts

# Install dependencies
cd frontend
npm install
npm install pinia axios
npm install --save-dev @vitejs/plugin-vue
```

#### Backend
```bash
# Initialize Python project with uv
cd /home/user/backend
uv init

# Add production dependencies
uv add fastapi uvicorn[standard] pydantic sqlalchemy aiosqlite

# Add development dependencies
uv add --dev pytest httpx
```

#### Database
- SQLite (built-in with Python, no separate installation)
- SQLAlchemy for ORM
- aiosqlite for async SQLite support

## Implementation Phases

### Phase 1: Foundation
Scaffold both frontend and backend projects, configure development environments, and verify both services can start successfully.

### Phase 2: Core Implementation
Implement database schema and models, build FastAPI endpoints, create Vue components and Pinia store.

### Phase 3: Integration & Polish
Connect frontend to backend API, add error handling and loading states, polish UI/UX, and validate end-to-end functionality.

## Step by Step Tasks

### 1. Bootstrap & Verify Stack

#### Backend Setup
- Navigate to `/home/user/` and create `backend` directory
- Initialize uv project: `cd backend && uv init`
- Add dependencies: `uv add fastapi uvicorn[standard] pydantic sqlalchemy aiosqlite`
- Add dev dependencies: `uv add --dev pytest httpx`
- Create directory structure: `mkdir -p src`
- Verify backend can start: Create basic FastAPI app in `src/main.py` with health endpoint
- Test: `cd /home/user/backend && uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000`

#### Frontend Setup
- Navigate to `/home/user/` and create frontend with Vite: `npm create vite@latest frontend -- --template vue-ts`
- Install dependencies: `cd frontend && npm install`
- Add Pinia and Axios: `npm install pinia axios`
- Configure Vite for proper host binding in `vite.config.ts`
- Verify frontend can start: `npm run dev -- --host 0.0.0.0 --port 5173`

### 2. Backend & Database Foundation

#### Database Schema
- Create `src/database.py`:
  - SQLAlchemy engine setup for SQLite (`sqlite+aiosqlite:///./todos.db`)
  - Define `Todo` table model with columns: id (int, primary key), text (string), completed (boolean), created_at (datetime)
  - Create async session maker
  - Add database initialization function

#### Backend Models
- Create `src/models.py`:
  - `TodoCreate` Pydantic model: text (str, min length 1, max length 500)
  - `TodoUpdate` Pydantic model: text (optional str), completed (optional bool)
  - `TodoResponse` Pydantic model: id (int), text (str), completed (bool), created_at (datetime)

#### CRUD Operations
- Create `src/crud.py`:
  - `get_todos()` - Fetch all todos ordered by created_at descending
  - `get_todo(id)` - Fetch single todo by ID
  - `create_todo(text)` - Create new todo with text
  - `update_todo(id, data)` - Update todo (toggle complete or edit text)
  - `delete_todo(id)` - Delete single todo
  - `delete_completed_todos()` - Delete all completed todos

#### API Endpoints
- Update `src/main.py`:
  - Configure CORS to allow frontend origin (http://localhost:5173)
  - `GET /api/todos` - List all todos
  - `POST /api/todos` - Create new todo (expects JSON body with "text")
  - `PUT /api/todos/{id}` - Update todo (expects JSON body with optional "text" and "completed")
  - `DELETE /api/todos/{id}` - Delete specific todo
  - `DELETE /api/todos/completed` - Delete all completed todos
  - Add startup event to initialize database tables

### 3. Frontend Foundation

#### Environment Configuration
- Create `.env` file in frontend directory:
  ```
  VITE_API_BASE_URL=http://localhost:8000
  ```

#### API Client
- Create `src/services/api.ts`:
  - Configure Axios instance with base URL from environment variable
  - Export methods for all API endpoints:
    - `fetchTodos()` - GET /api/todos
    - `createTodo(text)` - POST /api/todos
    - `updateTodo(id, data)` - PUT /api/todos/{id}
    - `deleteTodo(id)` - DELETE /api/todos/{id}
    - `deleteCompletedTodos()` - DELETE /api/todos/completed

#### Pinia Store
- Create `src/stores/todoStore.ts`:
  - State: todos array, loading boolean, error string, filter (all/active/completed)
  - Getters:
    - `filteredTodos` - Returns todos based on current filter
    - `activeTodoCount` - Count of incomplete todos
    - `hasCompletedTodos` - Boolean if any completed todos exist
  - Actions:
    - `loadTodos()` - Fetch todos from API
    - `addTodo(text)` - Create new todo
    - `toggleTodo(id)` - Toggle completion status
    - `removeTodo(id)` - Delete todo
    - `clearCompleted()` - Delete all completed todos
    - `setFilter(filter)` - Update active filter

#### Update main.ts
- Import and configure Pinia
- Create and mount Pinia store to app instance

### 4. Feature Implementation

#### TodoInput Component
- Create `src/components/TodoInput.vue`:
  - Input field with v-model binding
  - "Add" button that calls store's `addTodo` action
  - Enter key support
  - Clear input after successful add
  - Disable during loading state
  - Show validation errors (minimum 1 character)

#### TodoItem Component
- Create `src/components/TodoItem.vue`:
  - Props: todo object
  - Checkbox for completion toggle (calls `toggleTodo`)
  - Todo text with strike-through styling for completed items
  - Delete button (calls `removeTodo`)
  - Hover effects for better UX

#### TodoList Component
- Create `src/components/TodoList.vue`:
  - Compose TodoInput and TodoItem components
  - Filter buttons: All/Active/Completed (updates store filter)
  - Active todo counter display (e.g., "3 items left")
  - "Clear completed" button (only visible if completed todos exist)
  - Loading spinner while fetching data
  - Error message display
  - Empty state message when no todos exist

#### App Component
- Update `src/App.vue`:
  - Main layout structure with header
  - Render TodoList component
  - Apply global styling
  - Call `loadTodos()` on component mount

### 5. Integration & Observability

#### CORS Configuration
- Ensure backend allows requests from `http://localhost:5173`
- Add proper headers for credentials if needed (not required for this simple app)

#### Error Handling
- Frontend: Catch API errors and display user-friendly messages in UI
- Backend: Return appropriate HTTP status codes and error messages
- Handle network failures gracefully

#### Loading States
- Show loading spinner during API calls
- Disable buttons during async operations
- Provide visual feedback for user actions

#### HTML Page Title
- Update `index.html` title to start with workflow ID: "gemini-cli-gemini-3--very_easy_todo_list - Todo List"

### 6. Testing & Verification

#### Backend Testing
- Create `tests/test_api.py`:
  - Test creating a todo (POST /api/todos)
  - Test fetching todos (GET /api/todos)
  - Test updating todo (PUT /api/todos/{id})
  - Test deleting todo (DELETE /api/todos/{id})
  - Test deleting completed todos (DELETE /api/todos/completed)
  - Test validation errors (empty text, invalid ID)
- Run tests: `cd /home/user/backend && uv run pytest -v`

#### Database Testing
- Verify database file is created: `ls /home/user/backend/todos.db`
- Test schema creation and data persistence
- Verify database survives server restarts

#### Frontend Testing
- Build production bundle: `cd /home/user/frontend && npm run build`
- Verify no build errors
- Check bundle size is reasonable

#### Full-Stack Integration
- Start backend: `cd /home/user/backend && uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000 &`
- Start frontend: `cd /home/user/frontend && npm run dev -- --host 0.0.0.0 --port 5173 &`
- Test complete user flow:
  1. Add several todos
  2. Mark some as complete
  3. Filter by Active/Completed/All
  4. Delete individual todo
  5. Clear all completed
  6. Refresh page and verify data persists
- Test external access via public URL

## Testing Strategy

### Backend
- **Unit Tests**: Test individual CRUD functions in isolation with test database
- **Integration Tests**: Test FastAPI routes end-to-end with TestClient
- **Validation Tests**: Verify Pydantic models reject invalid data
- **Database Tests**: Confirm schema creation and data persistence

### Database
- **Schema Validation**: Verify table structure matches expectations
- **Data Integrity**: Test constraints (unique IDs, required fields)
- **Persistence**: Confirm data survives server restarts

### Frontend
- **Build Tests**: Verify production build succeeds without errors
- **Component Tests**: Test individual Vue components with test utils (optional for this simple app)
- **Integration Tests**: Manual testing of complete user flows

### Combined
- **End-to-End Tests**: Start both services and validate complete user journeys
- **CORS Tests**: Verify frontend can communicate with backend
- **External Access**: Test application from outside sandbox using public URL

## Acceptance Criteria

1. Backend server starts successfully on port 8000
2. Frontend dev server starts successfully on port 5173
3. All API endpoints return correct responses with appropriate status codes
4. Database persists todos across server restarts
5. User can add new todos through the UI
6. User can mark todos as complete/incomplete
7. User can delete individual todos
8. User can clear all completed todos
9. Filter buttons (All/Active/Completed) work correctly
10. Active todo count displays accurately
11. Data persists after page refresh
12. Professional, modern UI with good UX
13. No console errors in browser
14. Application is accessible via public URL
15. HTML title starts with workflow ID "gemini-cli-gemini-3--very_easy_todo_list"

## Validation Commands

Execute these commands in order to validate the complete implementation:

```bash
# 1. Backend Validation
cd /home/user/backend
uv run pytest -v  # Run backend tests

# 2. Database Validation
ls -lh /home/user/backend/todos.db  # Verify database exists

# 3. Frontend Build Validation
cd /home/user/frontend
npm run build  # Verify production build succeeds

# 4. Start Backend Service
cd /home/user/backend
uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000 &

# 5. Test Backend Health
curl http://localhost:8000/api/todos  # Should return empty array initially

# 6. Start Frontend Service
cd /home/user/frontend
npm run dev -- --host 0.0.0.0 --port 5173 &

# 7. External Access Validation
# Get public URL and test from outside sandbox
curl <public-url>  # Should return HTML

# 8. End-to-End Flow
# Use browser to test complete user journey:
# - Add todo
# - Toggle completion
# - Delete todo
# - Filter todos
# - Clear completed
# - Refresh and verify persistence
```

## Notes

- The application uses modern async patterns throughout (FastAPI async routes, aiosqlite)
- SQLite is sufficient for a single-user application; no complex database setup required
- Pinia provides excellent TypeScript support and devtools integration
- All dependencies are pinned to ensure reproducible builds
- The frontend will proxy API requests to avoid CORS issues in production
- Consider adding these features in future iterations:
  - Edit todo text inline
  - Due dates and priorities
  - Categories/tags
  - Search/filter by text
  - Keyboard shortcuts
  - Dark mode toggle
- The application follows Vue 3 Composition API best practices
- FastAPI automatic documentation available at http://localhost:8000/docs
