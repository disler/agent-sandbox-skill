Create a **Log Analysis Assistant** that turns raw log files into actionable insights.

**Core Features:**
1.  **File Upload**: Drag and drop support for large `.log` or `.txt` files.
2.  **Pattern Matching**: Users can define regex patterns (e.g., `ERROR .*`, `WARN .*`) to highlight lines.
3.  **Anomaly Detection**: A basic algorithm that groups similar log lines and flags "rare" events (appearing < 1% of the time).
4.  **Visualization**: A time-series bar chart showing the frequency of log entries per minute/hour (requires parsing timestamps).
5.  **Export**: Ability to export the "Filtered View" to a new text file.

**Technical Requirements:**
-   Leverage Python's strong text processing capabilities (regex, string manipulation) for pattern matching and anomaly detection.
-   Install a charting library for time-series visualization of log frequency.

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
