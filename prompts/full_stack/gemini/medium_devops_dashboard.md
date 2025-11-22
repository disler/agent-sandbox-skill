Build a **Unified DevOps Dashboard** that serves as a single pane of glass for tracking deployment statuses across multiple environments.

**Core Features:**
1.  **Deployment Tracking**: Ingest webhooks from GitHub Actions or GitLab CI to display current build status (Pending, Success, Failed) for multiple projects.
2.  **Environment View**: distinct columns for Dev, Staging, and Production environments.
3.  **Log Stream**: A detailed view that allows clicking into a specific build to see the tail of the build logs (simulated or stored in the DB).
4.  **Rollback Trigger**: A "Rollback" button next to production deployments that triggers a specific API hook (mocked for now).
5.  **Metrics**: A simple chart showing "Success Rate" and "Average Build Time" over the last 30 days.

**Technical Requirements:**
-   Install `chart.js` or similar for displaying "Success Rate" and "Average Build Time" metrics.
-   Use polling or WebSockets to update build statuses without refreshing.

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
