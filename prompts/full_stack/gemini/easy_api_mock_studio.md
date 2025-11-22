Develop a **Visual API Mocking Studio** designed for frontend developers who need to prototype UI before the backend is ready.

**Core Features:**
1.  **Route Designer**: A UI to define HTTP methods (GET, POST, PUT, DELETE) and URL paths (e.g., `/users/:id`).
2.  **Response Builder**: A JSON editor to define the expected response body. Support "dynamic" fields using a faker syntax (e.g., `{{name}}`, `{{uuid}}`) that generates random data on each hit.
3.  **Latency Simulator**: A slider to inject artificial delay (0ms - 5000ms) to test frontend loading states.
4.  **Error Injection**: A toggle to randomly return 400/500 error codes X% of the time.
5.  **Live Server**: A "Start Server" button that spins up a temporary mock server (or handles requests via the main backend routing) based on the defined configuration.

**Technical Requirements:**
-   Focus on a clean, IDE-like interface.
-   The backend must be able to match incoming requests to user-defined paths stored in the database.

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
