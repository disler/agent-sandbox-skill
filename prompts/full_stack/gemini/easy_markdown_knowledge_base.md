Build a **Git-Backed Markdown Knowledge Base** (a "Second Brain" app).

**Core Features:**
1.  **Markdown Editor**: A rich text editor that saves content as Markdown. Support standard syntax + code blocks.
2.  **Wiki-Links**: Support `[[Link]]` syntax to create internal links between documents.
3.  **Graph View**: A visual node-link diagram showing how documents are connected via their links.
4.  **Full-Text Search**: Fast search functionality to find notes by content or title.
5.  **Git Sync**: A "Sync" button that commits and pushes changes to a configured Git repository (can simulate this with local file operations if needed).

**Technical Requirements:**
-   Install `marked` (or similar) for markdown rendering.
-   The "Database" is primarily the file system (directory of .md files), but use SQLite for metadata/caching the graph structure for performance.

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
