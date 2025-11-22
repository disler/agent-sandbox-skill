Develop a **Cron Job Heartbeat Monitor** (similar to Dead Man's Snitch).

**Core Features:**
1.  **Monitor Management**: Create a new "Monitor" which generates a unique URL (UUID).
2.  **Listening Endpoint**: A `GET /ping/:uuid` endpoint. When hit, it records a success event.
3.  **Alert Rules**: Users define an "Expected Interval" (e.g., every 5 mins). If no ping is received within (Interval + Grace Period), the monitor status turns to "DOWN".
4.  **Dashboard**: A grid view of all monitors with Red/Green status indicators.
5.  **Alert Simulation**: Since we can't easily send real emails, log an "ALERT" message to the server console and show a notification toast in the UI when a monitor fails.

**Technical Requirements:**
-   Install `apscheduler` or implement a simple background loop to check for stale monitors.

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
