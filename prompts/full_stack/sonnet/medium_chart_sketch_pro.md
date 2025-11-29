# Chart Sketch Pro - Visual Story Builder

Build a comprehensive visual communication tool for creating chart collections, dashboards, and presentations using intuitive slider-based data entry. Designed for professionals who need to communicate ideas through clean visuals without wrestling with spreadsheets.

## Value Proposition

Turn abstract ideas into compelling visuals in minutes. Create individual charts or combine them into dashboards and presentations. Level-based sliders let you focus on relationships and proportions, not precise numbers. Perfect for strategy meetings, stakeholder updates, pitch decks, and team alignment.

## Core Features

### Chart Types (6 Types)
- **Bar Chart**: Vertical or horizontal bars with slider-controlled heights
- **Stacked Bar**: Multiple series per category showing composition
- **Pie Chart**: Segments with slider-controlled proportions
- **Donut Chart**: Pie variant with center label/metric
- **Line Chart**: Points connected by lines showing trends
- **Area Chart**: Filled line chart for emphasis

### Slider-Based Data Entry
- Each data point uses a **level slider** (not numeric input)
- **Standard Mode**: 5 levels (Very Low → Low → Medium → High → Very High)
- **Extended Mode**: 10 levels for finer granularity
- **Comparison Mode**: Negative-to-positive scale (-5 to +5)
- Visual level indicator with color feedback
- Add/remove data points (2-12 points per chart)
- Drag-and-drop reordering
- Bulk level adjustment (shift all points up/down)

### Multi-Series Support
- Add multiple data series to bar and line charts
- Each series has its own color and name
- Series legend with toggle visibility
- Compare "Before/After", "Plan/Actual", "Team A/Team B"
- Up to 4 series per chart

### Text Inputs (Minimal)
- **Chart Title**: Main chart heading
- **Subtitle**: Optional secondary description
- **X-Axis Label**: Horizontal axis label
- **Y-Axis Label**: Vertical axis label
- **Data Point Names**: Label for each data point (max 25 chars)
- **Series Names**: Label for each data series
- **Annotations**: Optional callout text on specific points

### Collections & Dashboards
- Group related charts into **Collections**
- Create **Dashboards** with 2-6 charts in grid layout
- Dashboard templates: 2x1, 2x2, 3x2, 1+2 sidebar
- Drag charts to reorder within dashboard
- Collection cover image auto-generated from first chart
- Collection descriptions and tags

### Chart Annotations
- Add text callouts pointing to specific data points
- Highlight zones (shade regions of chart)
- Trend lines (auto-fit or manual)
- Reference lines (horizontal markers like "Target", "Average")
- Emoji reactions on data points for emphasis

### Themes & Styling
- **5 Built-in Themes**:
  - Sketch Pad (warm, friendly)
  - Corporate (professional blues)
  - Bold (high contrast, vibrant)
  - Minimal (black, white, gray)
  - Dark Mode (dark background, light elements)
- Per-chart theme override
- Custom accent color picker
- Font size scaling (S, M, L)

### Save & Organize
- Save individual charts or full collections
- Auto-save drafts every 30 seconds
- Version history (last 5 saves)
- Duplicate charts and collections
- Move charts between collections
- Star/favorite important charts
- Search charts by title or tag
- Filter by chart type or collection

### Export & Share
- **Download Options**:
  - PNG (standard and @2x retina)
  - SVG vector
  - PDF (single chart or full dashboard)
- Copy chart to clipboard
- Export collection as ZIP (all charts)
- **Presentation Mode**: Full-screen slideshow of collection
- Generate shareable link (read-only view)

## UI Theme: "Sketch Pad Pro"

An elevated version of the warm, approachable design with professional polish.

### Color Palette
- **Background**: Warm white (#FDFBF7)
- **Surface/Cards**: Pure white (#FFFFFF)
- **Sidebar**: Light warm gray (#F5F3EF)
- **Primary**: Soft coral (#E07A5F)
- **Secondary**: Sage green (#81B29A)
- **Tertiary**: Dusty blue (#3D5A80)
- **Accent**: Golden honey (#F2CC8F)
- **Text Primary**: Charcoal (#2D3142)
- **Text Secondary**: Warm gray (#6B7280)
- **Text Muted**: Light gray (#9CA3AF)
- **Border**: Light gray (#E5E7EB)
- **Success**: Fresh green (#10B981)
- **Warning**: Amber (#F59E0B)
- **Error**: Rose (#EF4444)

### Chart Color Palettes
**Default Palette**:
```
Coral:    #E07A5F
Sage:     #81B29A
Dusty:    #3D5A80
Honey:    #F2CC8F
Lavender: #9A8C98
Teal:     #4ECDC4
Peach:    #F7A072
Slate:    #5C6B73
Mint:     #A8E6CF
Plum:     #6C5B7B
Marigold: #F4A261
Ocean:    #457B9D
```

**Corporate Palette**:
```
Navy:     #1E3A5F
Steel:    #4A6FA5
Sky:      #7BA3CC
Silver:   #A8B8C8
Charcoal: #3D4F5F
```

**Bold Palette**:
```
Electric: #FF6B6B
Cyan:     #4ECDC4
Yellow:   #FFE66D
Magenta:  #C44569
Lime:     #95E1D3
```

### Typography
- **Font Family**: Inter (UI), DM Sans (chart titles)
- **Page Title**: 28px, Bold, Charcoal
- **Chart Title**: 22px, Semi-bold, Charcoal
- **Chart Subtitle**: 14px, Regular, Warm gray
- **Axis Labels**: 13px, Medium, Warm gray
- **Data Labels**: 11px, Medium, Charcoal
- **Legend**: 12px, Regular, Charcoal
- **UI Text**: 14px, Regular, Charcoal
- **Small Text**: 12px, Regular, Warm gray

### Layout & Spacing
- Sidebar width: 280px (collapsible)
- Card padding: 24px
- Card gap: 16px
- Border radius: 12px (cards), 8px (buttons), 4px (inputs)
- Shadow levels:
  - Cards: 0 2px 8px rgba(0,0,0,0.06)
  - Elevated: 0 4px 16px rgba(0,0,0,0.1)
  - Modals: 0 8px 32px rgba(0,0,0,0.15)

## Technical Requirements

### Database Schema

**Collections**:
- id (primary key)
- name (text)
- description (text, nullable)
- cover_chart_id (foreign key, nullable)
- is_starred (boolean)
- created_at (timestamp)
- updated_at (timestamp)

**Charts**:
- id (primary key)
- collection_id (foreign key, nullable)
- title (text)
- subtitle (text, nullable)
- chart_type (text: 'bar', 'stacked_bar', 'pie', 'donut', 'line', 'area')
- orientation (text: 'vertical', 'horizontal')
- x_label (text, nullable)
- y_label (text, nullable)
- theme (text: 'sketch_pad', 'corporate', 'bold', 'minimal', 'dark')
- level_mode (text: 'standard', 'extended', 'comparison')
- show_legend (boolean)
- position (integer: order in collection)
- is_starred (boolean)
- created_at (timestamp)
- updated_at (timestamp)

**DataSeries**:
- id (primary key)
- chart_id (foreign key)
- name (text)
- color (text: hex color)
- position (integer: order in legend)

**DataPoints**:
- id (primary key)
- series_id (foreign key)
- name (text)
- level (integer: -10 to 10 depending on mode)
- position (integer: order in chart)

**Annotations**:
- id (primary key)
- chart_id (foreign key)
- type (text: 'callout', 'highlight', 'trendline', 'reference')
- text (text, nullable)
- target_point_id (foreign key, nullable)
- config (json: position, style, etc.)

**Dashboards**:
- id (primary key)
- collection_id (foreign key)
- name (text)
- layout (text: '2x1', '2x2', '3x2', 'sidebar')
- created_at (timestamp)

**DashboardCharts**:
- id (primary key)
- dashboard_id (foreign key)
- chart_id (foreign key)
- position (integer: slot in grid)

**ChartVersions**:
- id (primary key)
- chart_id (foreign key)
- snapshot (json: full chart state)
- created_at (timestamp)

### Backend API

**Collections**:
- `GET /api/collections` - List all collections
- `GET /api/collections/{id}` - Get collection with charts
- `POST /api/collections` - Create collection
- `PUT /api/collections/{id}` - Update collection
- `DELETE /api/collections/{id}` - Delete collection (and charts)
- `POST /api/collections/{id}/star` - Toggle star

**Charts**:
- `GET /api/charts` - List all charts (with filters)
- `GET /api/charts/{id}` - Get chart with series, points, annotations
- `POST /api/charts` - Create chart
- `PUT /api/charts/{id}` - Update chart
- `DELETE /api/charts/{id}` - Delete chart
- `POST /api/charts/{id}/duplicate` - Duplicate chart
- `PUT /api/charts/{id}/move` - Move to different collection
- `POST /api/charts/{id}/star` - Toggle star

**Data Series**:
- `POST /api/charts/{id}/series` - Add series
- `PUT /api/charts/{id}/series/{series_id}` - Update series
- `DELETE /api/charts/{id}/series/{series_id}` - Delete series

**Data Points**:
- `POST /api/series/{id}/points` - Add point
- `PUT /api/series/{id}/points/{point_id}` - Update point
- `DELETE /api/series/{id}/points/{point_id}` - Delete point
- `PUT /api/series/{id}/points/reorder` - Reorder points
- `PUT /api/series/{id}/points/bulk-adjust` - Shift all levels

**Annotations**:
- `POST /api/charts/{id}/annotations` - Add annotation
- `PUT /api/charts/{id}/annotations/{ann_id}` - Update annotation
- `DELETE /api/charts/{id}/annotations/{ann_id}` - Delete annotation

**Dashboards**:
- `GET /api/dashboards` - List dashboards
- `GET /api/dashboards/{id}` - Get dashboard with charts
- `POST /api/dashboards` - Create dashboard
- `PUT /api/dashboards/{id}` - Update dashboard
- `DELETE /api/dashboards/{id}` - Delete dashboard
- `PUT /api/dashboards/{id}/charts` - Update chart positions

**Export**:
- `GET /api/charts/{id}/export?format=png&scale=1|2` - PNG export
- `GET /api/charts/{id}/export?format=svg` - SVG export
- `GET /api/charts/{id}/export?format=pdf` - PDF export
- `GET /api/dashboards/{id}/export?format=pdf` - Dashboard PDF
- `GET /api/collections/{id}/export` - ZIP of all charts

**Versions**:
- `GET /api/charts/{id}/versions` - List versions
- `POST /api/charts/{id}/versions/{version_id}/restore` - Restore version

### Frontend

**Layout**:
- Collapsible left sidebar: Collections tree + chart list
- Main canvas area: Active chart/dashboard editor
- Right panel: Context-sensitive properties (chart settings, data editor)
- Top toolbar: Chart type, theme, export actions

**Key Components**:

*Sidebar*:
- Collection tree with expand/collapse
- Chart thumbnails within collections
- Star filter toggle
- Search input with instant results
- "New Collection" and "New Chart" buttons

*Chart Canvas*:
- Large preview area with real-time rendering
- Zoom controls (fit, 100%, 150%)
- Pan/scroll for large dashboards
- Click-to-select annotations

*Data Editor Panel*:
- Series tabs (for multi-series charts)
- Data point list with:
  - Drag handle
  - Name input
  - Level slider (with mode indicator)
  - Color swatch
  - Annotation icon (if has annotation)
  - Delete button
- "Add Point" and "Add Series" buttons
- Bulk actions: shift all up/down

*Chart Settings Panel*:
- Title and subtitle inputs
- Axis label inputs
- Chart type selector (icon grid)
- Orientation toggle (bar charts)
- Level mode selector
- Theme picker
- Legend toggle
- Font size selector

*Annotation Tools*:
- Annotation mode toggle
- Click point to add callout
- Drag to create highlight zone
- Reference line input (label + level)

*Dashboard Editor*:
- Layout template picker
- Drag charts from sidebar into slots
- Resize handles on chart panels
- Preview mode toggle

**Chart Rendering**:
- Install `chart.js` with plugins for annotations
- Install `chartjs-plugin-annotation` for reference lines
- Real-time updates with 60fps animation
- Level labels on axes based on mode
- Smooth transitions on all changes
- Theme-aware colors and styling

**Export Implementation**:
- Use html2canvas for PNG export (1x and 2x)
- Generate SVG from Chart.js
- Install `jspdf` for PDF generation
- JSZip for collection export

## User Personas

**Product Manager**: Creates roadmap visualizations and priority charts for stakeholder presentations

**Team Lead**: Builds sprint dashboards showing team capacity and workload distribution

**Consultant**: Generates client-ready visuals for strategy decks without touching Excel

**Educator**: Creates teaching materials with clear, level-based comparisons

**Founder**: Pitches ideas to investors with compelling visual narratives

## Success Metrics

- Create multi-series chart in under 60 seconds
- Dashboard with 4 charts loads in under 1 second
- Export PNG/SVG completes in under 2 seconds
- PDF export for 6-chart dashboard in under 5 seconds
- Real-time slider updates render at 60fps
- Auto-save triggers within 30 seconds of change
- Version history loads instantly
- Search returns results in under 200ms

## Bonus Features (Future Enhancements)

- Team collaboration with shared collections
- Comments on charts and annotations
- Chart templates library (pre-built starting points)
- Animation presets for presentations
- Voice-over recording for slideshows
- Embed charts in external pages (iframe/script)
- API access for programmatic chart creation
- Custom level labels (replace "High/Low" with domain terms)
- Branching/comparison dashboards (A vs B scenarios)
- Integration with presentation tools (Google Slides, PowerPoint)
- Mobile companion app for quick edits
- Offline mode with sync

## Implementation Notes

This application builds on the "easy" Chart Sketch by adding:
1. **Multi-series support** - Compare multiple data sets
2. **Collections & Dashboards** - Organize and combine charts
3. **6 chart types** - More visualization options
4. **Annotations** - Add context and callouts
5. **5 themes** - Professional styling options
6. **Version history** - Never lose work
7. **Advanced export** - PDF and dashboard export

The core philosophy remains: **levels, not numbers**. Keep data entry fast and intuitive while providing professional-quality output.

## UI Design

Build the "Sketch Pad Pro" theme interface with:
- Warm white background (#FDFBF7) with subtle paper texture
- Three-panel layout: sidebar (280px), canvas (flexible), properties (320px)
- Collapsible panels for focused work
- Card-based UI with soft shadows
- Coral (#E07A5F) primary for key actions
- DM Sans for titles, Inter for UI text
- Smooth 200ms transitions on panel toggles
- Keyboard shortcuts for power users (Cmd+S save, Cmd+D duplicate)
- Toast notifications for save/export feedback
- Drag-and-drop everywhere (reorder, move to collection, dashboard slots)
- Loading skeletons for async operations
- Responsive: sidebar collapses to icons on tablet, bottom sheet on mobile
