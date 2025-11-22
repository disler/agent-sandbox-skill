Develop a **Local-First Kanban Task Board** that prioritizes offline capability and state synchronization.

**Core Features:**
1.  **Board Layout**: Classic Todo / In Progress / Done columns.
2.  **Drag and Drop**: Smooth UI for moving cards between columns.
3.  **Offline Mode**: The app must function fully without the backend running. Changes queue up.
4.  **Sync Mechanism**: When online, the frontend sends a batch of changes to the backend. (Keep conflict resolution simple: last write wins).
5.  **Markdown Support**: Task descriptions support markdown rendering.

**Technical Requirements:**
-   Install `dnd-kit` (or similar) for drag-and-drop functionality.
-   Use `localStorage` for offline persistence.

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
