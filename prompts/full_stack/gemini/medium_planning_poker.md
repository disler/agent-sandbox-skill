Build a **Real-time Agile Planning Poker** application for distributed teams.

**Core Features:**
1.  **Room Management**: Users can create a "Room" and share the URL with teammates.
2.  **Voting System**: Participants select a card (Fibonacci sequence: 1, 2, 3, 5, 8, 13, ?) to estimate a story.
3.  **Reveal Mechanism**: Votes remain hidden until the moderator clicks "Reveal Cards".
4.  **Spectator Mode**: Allow users to join as observers without voting rights.
5.  **Jira/Linear Import**: A form to "Import Ticket" (by text ID) that displays the ticket title/description on the central board.

**Technical Requirements:**
-   Use WebSockets for real-time state synchronization between participants.
-   In-memory storage (Redis or Python dict) is fine for active rooms, but persist room history in the database.

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
