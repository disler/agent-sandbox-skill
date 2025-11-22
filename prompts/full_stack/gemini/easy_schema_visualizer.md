Build a **Database Schema Visualizer and Annotation Tool**.

**Core Features:**
1.  **Connection Manager**: Input fields for DB credentials (host, user, pass, dbname). For safety, restrict to localhost or SQLite files initially.
2.  **Schema Extraction**: Backend queries the database `information_schema` (or equivalent) to get tables, columns, and foreign keys.
3.  **Visualizer**: Render an Entity-Relationship Diagram (ERD) on the canvas. Nodes = Tables, Edges = Foreign Keys.
4.  **Annotation Layer**: Allow users to click a table/column and add a "Note" or "Description" which is saved in the app's local DB (not the target DB).
5.  **Search**: Filter the diagram to show only tables matching a search string.

**Technical Requirements:**
-   Install `@vue-flow/core` for entity-relationship diagramming.
-   Install `sqlalchemy` for database introspection and reflection capabilities.

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
