# Simple Notes App

Build a note-taking application where users can create, edit, and delete text notes. Each note has a title and body content.

## Core Features

### Note Management
- Create new note with title and body
- Edit existing note
- Delete note
- List all notes (showing title + preview)
- Click note to view/edit full content

### Display
- Sidebar with note list
- Main area for viewing/editing selected note
- Search notes by title

## Technical Requirements

### Database Schema
- Store notes with ID, title, body content, and update timestamp
- Primary key for each note record

### Backend API
- `GET /api/notes` - List all notes
- `GET /api/notes/{id}` - Get single note
- `POST /api/notes` - Create note
- `PUT /api/notes/{id}` - Update note
- `DELETE /api/notes/{id}` - Delete note

### Frontend
- Left sidebar: note list with search capability
- Right area: note editor (title + body textarea)
- "New Note" button for creating notes
- Save/Delete buttons for note management
- Search input for filtering notes
- Install `axios` for API requests

## Success Criteria
- Create notes with title and body
- Edit notes and see changes persist
- Delete notes
- Search filters note list
- Click note in list to load it

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


**Build time: ~15 minutes**
