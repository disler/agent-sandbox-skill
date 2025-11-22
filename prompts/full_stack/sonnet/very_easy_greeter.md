# Hello Greeter - Ultra-Simple Full-Stack

Build a simple greeting app: enter your name, click submit, backend returns personalized greeting and saves it to database. Display list of all previous greetings.

## Core Features

- Input field for name
- Submit button
- Display personalized greeting from backend
- Show list of all greetings (name + timestamp)
- Persist greetings in database

## Technical Requirements

### Database Schema
- Store greetings with name and timestamp
- Primary key for each greeting record

### Backend (2 endpoints)
- `POST /api/greet` - Accept name, save to DB, return greeting
- `GET /api/greetings` - Return all greetings

### Frontend
- Input field + submit button
- Display greeting message
- List of past greetings
- Fetch data from backend API

## Success Criteria
- Enter name → see "Hello, [name]!"
- Greetings persist and display in list
- Page refresh shows all previous greetings

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


**Build time: ~5 minutes**
