Create a self-hosted **Code Snippet Manager** inspired by Gist/SnippetsLab.

**Core Features:**
1.  **Snippet Library**: Create, Read, Update, Delete code snippets.
2.  **Syntax Highlighting**: Support multiple languages (Python, JS, Rust, Go) with automatic detection or manual selection.
3.  **Tagging System**: Add tags to snippets for easy filtering (e.g., #utility, #regex, #api).
4.  **Shareable Links**: Generate a public read-only link for a snippet (even if the app is local, simulate the URL structure).
5.  **CLI Companion**: Build a simple script (documented in the UI) that allows piping content to the server, e.g., `cat file.py | curl -X POST localhost:8000/api/snippet`.

**Technical Requirements:**
-   Install `monaco-editor` for code editing with syntax highlighting support.

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
