# Todo List - Simple Task Manager

Build a single-user todo list application with add, complete, and delete functionality. No authentication, just basic CRUD for todo items.

## Core Features

### Todo Management
- Add new todo with text description
- Mark todo as complete/incomplete (checkbox)
- Delete todo
- Display all todos (active and completed)
- Filter: All / Active / Completed

### Display
- Show todo count (e.g., "3 items left")
- Strike-through completed items
- Clear completed button (removes all completed)

## Technical Requirements

### Database Schema
- Store todos with ID, text, completed flag, and timestamp
- Primary key for each todo record

### Backend API
- `GET /api/todos` - List all todos
- `POST /api/todos` - Create new todo
- `PUT /api/todos/{id}` - Update todo (mark complete/incomplete)
- `DELETE /api/todos/{id}` - Delete todo
- `DELETE /api/todos/completed` - Delete all completed todos

### Frontend
- Input field + "Add" button
- Todo list with checkboxes for completion
- Delete button per item
- Filter buttons (All/Active/Completed)
- Todo counter display
- Install `axios` for API requests

## Success Criteria
- Add todos and see them in list
- Check/uncheck to toggle completion
- Delete individual todos
- Clear all completed todos
- Persist after page refresh

## UI Design
Build a modern, professional interface with:
- Clean, minimal design with proper spacing
- Modern color palette (primary/secondary/accent colors)
- Responsive layout that works on mobile and desktop
- Professional typography (readable fonts, clear hierarchy)
- Smooth transitions and hover effects
- Consistent component styling throughout
- Proper form validation with user feedback
- Loading states for async operations


**Build time: ~10-15 minutes**
