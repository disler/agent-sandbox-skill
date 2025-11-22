# File System Explorer

Build a web-based file system explorer that allows users to browse directories, view file contents, search files, and navigate through folder structures with a clean, intuitive interface.

## Core Features

### 1. Directory Tree Navigation
- Sidebar with expandable/collapsible folder tree
- Click folder to expand/collapse children
- Highlight currently selected folder
- Show folder icons and file count badges
- Breadcrumb navigation at top showing current path
- Home button to return to root directory

### 2. File Listing
- Main panel displays files and folders in current directory
- Grid view and list view toggle
- Sort by: name, size, type, date modified
- Show file metadata: size, type, last modified date
- File type icons (folder, text, image, code, etc.)
- Click folder to navigate into it
- Click file to preview/view it

### 3. File Viewer
- Modal or side panel for file preview
- Support multiple file types:
  - **Text files** (.txt, .md, .log): Display raw text
  - **Code files** (.js, .py, .html, .css, .json): Syntax highlighted view
  - **Images** (.png, .jpg, .gif, .svg): Image preview with zoom
  - **Markdown** (.md): Rendered markdown view
  - **JSON**: Pretty-printed with syntax highlighting
- Download file button
- Close/back button to return to file list
- File path and metadata display in viewer

### 4. Search & Filter
- Search bar to filter files by name
- Filter by file type (all, folders, images, code, documents)
- Real-time search results as you type
- Clear search button
- Highlight matching text in file names

### 5. File Upload
- Upload button to add files to current directory
- Drag-and-drop file upload
- Progress indicator during upload
- Support multiple file upload
- File size limit (e.g., 10MB per file)

### 6. Favorites & Recent
- Star/favorite frequently accessed folders
- Favorites list in sidebar
- Recently viewed files list
- Quick access to favorites and recent items

## Database Schema

```sql
-- Store directory structure
CREATE TABLE directories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    path TEXT UNIQUE NOT NULL,
    parent_id INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_id) REFERENCES directories(id) ON DELETE CASCADE
);

-- Store file metadata
CREATE TABLE files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    path TEXT UNIQUE NOT NULL,
    directory_id INTEGER NOT NULL,
    size INTEGER NOT NULL,
    mime_type TEXT NOT NULL,
    extension TEXT,
    last_modified DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (directory_id) REFERENCES directories(id) ON DELETE CASCADE
);

-- Track favorites
CREATE TABLE favorites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    directory_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (directory_id) REFERENCES directories(id) ON DELETE CASCADE
);

-- Track recently viewed files
CREATE TABLE recent_files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_id INTEGER NOT NULL,
    viewed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (file_id) REFERENCES files(id) ON DELETE CASCADE
);
```

## Backend API

**Directory Operations:**
- `GET /api/directories` - Get root directory tree
- `GET /api/directories/{id}` - Get directory details with children
- `GET /api/directories/{id}/files` - List files in directory
- `POST /api/directories` - Create new directory
- `DELETE /api/directories/{id}` - Delete directory

**File Operations:**
- `GET /api/files/{id}` - Get file metadata
- `GET /api/files/{id}/content` - Get file content (for preview)
- `GET /api/files/{id}/download` - Download file
- `POST /api/files/upload` - Upload file(s) to directory
- `DELETE /api/files/{id}` - Delete file

**Search:**
- `GET /api/search?q={query}&type={file_type}` - Search files and folders

**Favorites:**
- `GET /api/favorites` - List favorite directories
- `POST /api/favorites` - Add directory to favorites
- `DELETE /api/favorites/{id}` - Remove from favorites

**Recent:**
- `GET /api/recent` - Get recently viewed files
- `POST /api/recent/{file_id}` - Mark file as recently viewed

**File Serving:**
- `GET /static/files/{path}` - Serve actual files

## Frontend Structure

**Pages:**
1. **Explorer** (/)
   - Sidebar: Directory tree + favorites + recent
   - Main: File/folder listing with toolbar
   - Modal/Panel: File viewer

**Components:**
- DirectoryTree (recursive tree component)
- Breadcrumbs (navigation path)
- FileGrid (grid or list view)
- FileCard (file/folder item with icon and metadata)
- FileViewer (modal with content display)
- SearchBar (with filters)
- UploadZone (drag-drop area)
- Toolbar (view toggle, sort, upload button)
- FavoritesList (sidebar section)
- RecentFilesList (sidebar section)

## Key Implementation Details

**Backend:**
1. Initialize with a seed directory structure (create sample folders/files)
2. Store uploaded files in `/static/files/` directory
3. Implement recursive directory traversal for tree building
4. Handle MIME type detection for file type icons
5. Implement file size formatting (bytes → KB/MB)
6. Add pagination for large directories (limit 100 files per request)
7. Sanitize file paths to prevent directory traversal attacks

**Frontend:**
1. Install `axios` for API requests
2. Install `@vue-flow/core` or similar for tree visualization
3. Install `prismjs` for code syntax highlighting
4. Install `marked` for markdown rendering
5. Create Pinia store for:
   - Current directory state
   - File tree structure
   - Selected file
   - Favorites and recent items
6. Implement lazy loading for large directory trees
7. File upload with drag-and-drop using native File API
8. Breadcrumb navigation from path string

**File Type Detection:**
```python
import mimetypes

def get_file_type(filename):
    mime_type, _ = mimetypes.guess_type(filename)
    if mime_type:
        if mime_type.startswith('text'):
            return 'text'
        elif mime_type.startswith('image'):
            return 'image'
        elif mime_type in ['application/json', 'application/javascript']:
            return 'code'
    return 'unknown'
```

**Directory Tree Example:**
```python
def build_tree(parent_id=None):
    directories = db.query(
        "SELECT * FROM directories WHERE parent_id = ?",
        (parent_id,)
    )
    tree = []
    for directory in directories:
        tree.append({
            'id': directory.id,
            'name': directory.name,
            'path': directory.path,
            'children': build_tree(directory.id)
        })
    return tree
```

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

## Success Criteria

- Browse directory tree with expand/collapse
- Navigate through folders by clicking
- View file list in current directory
- Switch between grid and list view
- Search and filter files by name and type
- Preview text, code, images, and markdown files
- Download files
- Upload new files to directories
- Add folders to favorites for quick access
- View recently accessed files
- Breadcrumb navigation shows current path
- File metadata displayed accurately
- Smooth, responsive UI with good performance

**Build time: ~30-35 minutes**
