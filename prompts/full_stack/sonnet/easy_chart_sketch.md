# Chart Sketch - Visual Idea Communicator

Build a minimalist chart creation tool for quickly sketching bar charts, pie charts, and line charts using simple sliders. Designed for communicating high-level ideas through clean visuals, not precise data.

## Value Proposition

Communicate ideas visually in seconds. No spreadsheets, no data entry, no complexity. Just drag sliders to sketch proportions and relationships, then download or share your chart. Perfect for presentations, brainstorming, and explaining concepts.

## Core Features

### Chart Types
- **Bar Chart**: Vertical bars with slider-controlled heights
- **Pie Chart**: Segments with slider-controlled proportions
- **Line Chart**: Points with slider-controlled values connected by lines

### Slider-Based Data Entry
- Each data point uses a **level slider** (not numeric input)
- Slider range: 5 discrete levels (Very Low → Low → Medium → High → Very High)
- Visual indicator shows current level
- Add/remove data points (2-8 points per chart)
- Reorder data points via drag-and-drop

### Text Inputs (Minimal)
- **Chart Title**: Single text input for the chart name
- **X-Axis Label**: Label for horizontal axis (bar/line charts)
- **Y-Axis Label**: Label for vertical axis (bar/line charts)
- **Data Point Names**: Short label for each data point (max 20 chars)

### Save & Load
- Save charts to library with auto-generated thumbnail
- Load saved charts for editing
- Duplicate existing charts
- Delete saved charts
- Charts persist across sessions

### Export & Download
- Download as PNG image
- Download as SVG vector
- Copy chart to clipboard
- Quick share link (optional)

## UI Theme: "Sketch Pad"

A warm, approachable design that feels like sketching on paper.

### Color Palette
- **Background**: Warm white (#FDFBF7) - like quality paper
- **Surface/Cards**: Pure white (#FFFFFF) with soft shadow
- **Primary**: Soft coral (#E07A5F) - warm, friendly accent
- **Secondary**: Sage green (#81B29A) - calming secondary
- **Tertiary**: Dusty blue (#3D5A80) - professional touch
- **Text Primary**: Charcoal (#2D3142) - easy on eyes
- **Text Secondary**: Warm gray (#6B7280)
- **Border**: Light gray (#E5E7EB)

### Chart Colors (for data points)
```
Coral:    #E07A5F
Sage:     #81B29A
Dusty:    #3D5A80
Honey:    #F2CC8F
Lavender: #9A8C98
Teal:     #4ECDC4
Peach:    #F7A072
Slate:    #5C6B73
```

### Typography
- **Font Family**: Inter (clean, modern sans-serif)
- **Chart Title**: 24px, Semi-bold, Charcoal
- **Axis Labels**: 14px, Medium, Warm gray
- **Data Labels**: 12px, Regular, Charcoal
- **UI Text**: 14px, Regular, Charcoal

### Styling
- Rounded corners (8px for cards, 4px for buttons)
- Soft shadows (0 2px 8px rgba(0,0,0,0.08))
- Slider track: 6px height, rounded, light gray
- Slider thumb: 20px circle, primary color, subtle shadow
- Transitions: 150ms ease for all interactive elements

## Technical Requirements

### Database Schema
- **Charts** table:
  - id (primary key)
  - title (text)
  - chart_type (text: 'bar', 'pie', 'line')
  - x_label (text, nullable)
  - y_label (text, nullable)
  - created_at (timestamp)
  - updated_at (timestamp)
- **DataPoints** table:
  - id (primary key)
  - chart_id (foreign key)
  - name (text)
  - level (integer: 1-5)
  - position (integer: order in chart)
  - color (text: hex color)

### Backend API

**Charts**:
- `GET /api/charts` - List all saved charts
- `GET /api/charts/{id}` - Get chart with data points
- `POST /api/charts` - Create new chart
- `PUT /api/charts/{id}` - Update chart
- `DELETE /api/charts/{id}` - Delete chart

**Data Points**:
- `POST /api/charts/{id}/points` - Add data point
- `PUT /api/charts/{id}/points/{point_id}` - Update data point
- `DELETE /api/charts/{id}/points/{point_id}` - Delete data point
- `PUT /api/charts/{id}/points/reorder` - Reorder data points

**Export**:
- `GET /api/charts/{id}/export?format=png` - Download as PNG
- `GET /api/charts/{id}/export?format=svg` - Download as SVG

### Frontend

**Layout**:
- Left sidebar: Chart library (saved charts grid)
- Main area: Active chart canvas + controls
- Right panel: Data point editor (sliders + names)

**Components**:
- Chart type selector (3 icons: bar/pie/line)
- Title input field
- Axis label inputs (shown for bar/line only)
- Data point list with:
  - Drag handle for reordering
  - Name input (short text)
  - Level slider (5 positions)
  - Color indicator
  - Delete button
- "Add Data Point" button
- Save/Download buttons
- Chart preview that updates in real-time

**Chart Rendering**:
- Install `chart.js` for rendering
- Real-time updates as sliders move
- Smooth animations on value changes
- Level labels on Y-axis: "Very Low", "Low", "Medium", "High", "Very High"
- Clean, minimal chart styling matching theme

**Export Implementation**:
- Use html2canvas or chart.js native export for PNG
- Generate SVG from chart.js canvas
- Copy to clipboard using Clipboard API

## Success Criteria

- [ ] Create bar chart with 3+ data points
- [ ] Create pie chart with 3+ data points
- [ ] Create line chart with 3+ data points
- [ ] Sliders show 5 discrete levels
- [ ] Chart updates in real-time as sliders move
- [ ] Save chart to library
- [ ] Load chart from library
- [ ] Download chart as PNG
- [ ] Download chart as SVG
- [ ] Data persists after page refresh
- [ ] Theme matches "Sketch Pad" design spec

## Testing

### Manual Test Flow
1. Open app → empty library, default bar chart canvas
2. Enter title: "Team Priorities"
3. Add 4 data points: "Features", "Bugs", "Docs", "Testing"
4. Adjust sliders to different levels
5. Verify chart updates in real-time
6. Save chart → appears in library
7. Switch to pie chart type → same data renders as pie
8. Download as PNG → file saves correctly
9. Refresh page → saved chart still in library
10. Load saved chart → all data restored

### Validation
```bash
# List charts
curl http://localhost:8000/api/charts

# Create chart
curl -X POST http://localhost:8000/api/charts \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Chart","chart_type":"bar"}'

# Verify database
sqlite3 charts.db "SELECT * FROM charts"
```

## Why This Works

- **Fast**: Sliders are faster than typing numbers
- **Intuitive**: Levels communicate relative importance
- **Focused**: No complex options, just essential features
- **Portable**: Download and use anywhere
- **Persistent**: Save your work and come back later

## UI Design

Build the "Sketch Pad" theme interface with:
- Warm white background (#FDFBF7) like quality paper
- Clean cards with soft shadows for chart and controls
- Coral (#E07A5F) primary accent for buttons and sliders
- Inter font family throughout
- Rounded corners (8px) on all containers
- Smooth 150ms transitions on all interactive elements
- Clear visual hierarchy between title, controls, and chart
- Responsive layout: sidebar collapses on mobile
- Loading states for save/load/export operations

**Build time: ~20 minutes**
