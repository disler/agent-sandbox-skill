# SQLite Super Table - Universal CRUD Interface

Build a simple full-stack application that provides a universal CRUD interface for any SQLite database. Users can select tables, view all rows, and perform create, read, update, and delete operations with a clean, responsive UI.

## Value Proposition

A lightweight database admin tool for SQLite that runs in the browser. No installation, no configuration - just point it at a SQLite database and start managing your data. Perfect for development, testing, and quick data manipulation.

## Core Features

### Table Selection & Navigation
- Dropdown or sidebar listing all tables in the database
- Show table schema (column names and types) when selected
- Display row count for each table
- Search/filter table list if there are many tables

### Data Grid View
- Display all rows in the selected table in a data grid
- Show column headers with data types
- Paginated view (25, 50, 100 rows per page)
- Sort by any column (ascending/descending)
- Row highlighting on hover
- Empty state message when table has no rows

### CRUD Operations

#### Create
- "Add New Row" button that opens a modal/form
- Auto-generate form fields based on table schema
- Input validation based on column types
- **"Create Random Row" button** for quick test data generation
  - Auto-fills fields with appropriate random data (strings, numbers, booleans)
  - Respects column types and constraints
  - Useful for testing and development

#### Read
- Click any row to view full details in a modal
- Display all column values in a readable format
- Handle NULL values gracefully

#### Update
- "Edit" button on each row
- Pre-populate form with existing values
- Validate changes before saving
- Show confirmation message on success

#### Delete
- "Delete" button on each row
- Confirmation dialog before deletion
- Success notification after deletion
- Refresh grid automatically

### Real-time Feedback
- Loading states for all operations
- Success/error notifications (toast messages)
- Validation error messages on forms
- Optimistic UI updates where appropriate

## Technical Considerations

### Frontend Requirements
- Clean, minimal UI with good UX
- Responsive data grid/table component for displaying rows
- Modal dialogs for create/edit/view operations
- Install `axios` for HTTP requests to backend
- Form validation with error messages
- Toast notifications for user feedback
- Loading spinners during API calls

### Backend Requirements
- API endpoint to list all tables: `GET /api/tables`
- API endpoint for table schema: `GET /api/tables/{table_name}/schema`
- CRUD endpoints for each table:
  - `GET /api/tables/{table_name}/rows` - List all rows (with pagination)
  - `GET /api/tables/{table_name}/rows/{id}` - Get single row
  - `POST /api/tables/{table_name}/rows` - Create row
  - `PUT /api/tables/{table_name}/rows/{id}` - Update row
  - `DELETE /api/tables/{table_name}/rows/{id}` - Delete row
- Random data generation endpoint: `POST /api/tables/{table_name}/rows/random`
- Implement SQL injection protection
- Proper error handling and validation

### Database Schema
- Use an existing SQLite database file or create a sample one
- Initial seed data with 2-3 example tables:
  - **users** table (id, name, email, created_at)
  - **posts** table (id, user_id, title, content, published)
  - **tags** table (id, name, color)
- Support for common SQLite data types: INTEGER, TEXT, REAL, BLOB, NULL

### Random Data Generation
For the "Create Random Row" feature, generate appropriate data by type:
- **INTEGER**: Random number between 1-1000
- **TEXT**: Random string or Lorem ipsum (5-20 words)
- **REAL**: Random decimal number
- **BOOLEAN** (stored as INTEGER): 0 or 1
- **DATE/DATETIME**: Current timestamp or random recent date
- **Email fields**: generated email like `user123@example.com`
- **NULL fields**: Randomly decide if nullable fields should be NULL (20% chance)

## User Personas

**Developer**: Quickly inspects database during development without opening SQLite tools

**QA Tester**: Creates test data rapidly with random row generation for testing edge cases

**Data Analyst**: Views and modifies data in development/staging databases

## Success Metrics
- Table listing loads in under 200ms
- Data grid displays 100 rows without lag
- CRUD operations complete in under 500ms
- Random row generation works for all common data types
- UI is intuitive with zero learning curve
- Works on desktop and tablet screen sizes

## Bonus Features (Future Enhancements)
- Export table data as CSV or JSON
- Import data from CSV
- Execute custom SQL queries
- Table relationship visualization
- Bulk delete with checkboxes
- Column filtering and search
- Dark mode support
- Copy row data to clipboard
- Duplicate row functionality

## Implementation Notes

Keep this application **simple and focused**. The goal is to have a working full-stack CRUD app that:
1. Demonstrates frontend ↔ backend ↔ database integration
2. Provides all basic CRUD operations
3. Includes the "random row" testing feature
4. Has a clean, usable interface
5. Serves as a baseline for testing the full-stack workflow

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

