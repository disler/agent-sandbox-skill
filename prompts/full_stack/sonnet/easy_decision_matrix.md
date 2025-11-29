# Decision Matrix - Weighted Choice Visualizer

Build a simple decision-making tool that helps users compare options using weighted criteria with slider-based scoring. No spreadsheets, no complex math - just drag sliders to see which option wins.

## Value Proposition

Make confident decisions in minutes. Whether choosing between job offers, tech stacks, vendors, or product features - weight what matters, score your options, and see the winner instantly. Perfect for team alignment and stakeholder buy-in.

## Core Features

### Decision Setup
- **Decision Title**: What are you deciding? (e.g., "Which framework to use?")
- **Options**: Add 2-6 options to compare (e.g., "React", "Vue", "Svelte")
- **Criteria**: Add 2-8 criteria to evaluate (e.g., "Learning curve", "Performance", "Community")

### Slider-Based Scoring
- **Criteria Weight**: How important is this criterion? (5 levels: Not Important → Critical)
- **Option Score**: How well does this option meet this criterion? (5 levels: Poor → Excellent)
- Visual weight indicators show relative importance
- Scores update results in real-time

### Results Visualization
- **Winner Banner**: Clear highlight of the winning option
- **Bar Chart**: Weighted scores for all options
- **Breakdown Table**: See how each option scored per criterion
- **Score Gap**: How close was the decision? (landslide vs. close call)

### Save & Share
- Save decisions to library
- Load and revise past decisions
- Duplicate decisions for "what if" scenarios
- Export results as PNG image

## UI Theme: "Clear Choice"

A clean, confident design that brings clarity to complex decisions.

### Color Palette
- **Background**: Cool white (#F8FAFC)
- **Surface/Cards**: Pure white (#FFFFFF)
- **Primary**: Confident blue (#3B82F6) - trust, clarity
- **Winner**: Victory green (#10B981) - success, go
- **Accent**: Warm amber (#F59E0B) - attention, highlight
- **Text Primary**: Slate (#1E293B)
- **Text Secondary**: Gray (#64748B)
- **Border**: Light slate (#E2E8F0)
- **Poor Score**: Rose (#F43F5E)
- **Excellent Score**: Emerald (#10B981)

### Score Level Colors (gradient)
```
Poor:      #F43F5E (rose)
Fair:      #FB923C (orange)
Good:      #FBBF24 (amber)
Very Good: #84CC16 (lime)
Excellent: #10B981 (emerald)
```

### Typography
- **Font Family**: Inter
- **Decision Title**: 24px, Bold, Slate
- **Option Names**: 16px, Semi-bold, Slate
- **Criteria Names**: 14px, Medium, Gray
- **Score Labels**: 12px, Medium, matching score color
- **Winner Text**: 18px, Bold, Victory green

### Styling
- Rounded corners (12px cards, 6px buttons)
- Soft shadows (0 1px 3px rgba(0,0,0,0.1))
- Slider track: 8px height, rounded, light gradient
- Slider thumb: 24px circle, white with colored border
- Winner card: Green left border (4px), subtle green tint background
- Transitions: 200ms ease for all score updates

## Technical Requirements

### Database Schema
- **Decisions** table:
  - id (primary key)
  - title (text)
  - created_at (timestamp)
  - updated_at (timestamp)
- **Options** table:
  - id (primary key)
  - decision_id (foreign key)
  - name (text)
  - position (integer)
- **Criteria** table:
  - id (primary key)
  - decision_id (foreign key)
  - name (text)
  - weight (integer: 1-5)
  - position (integer)
- **Scores** table:
  - id (primary key)
  - option_id (foreign key)
  - criteria_id (foreign key)
  - score (integer: 1-5)

### Backend API

**Decisions**:
- `GET /api/decisions` - List all decisions
- `GET /api/decisions/{id}` - Get decision with options, criteria, scores
- `POST /api/decisions` - Create decision
- `PUT /api/decisions/{id}` - Update decision title
- `DELETE /api/decisions/{id}` - Delete decision
- `POST /api/decisions/{id}/duplicate` - Duplicate decision

**Options**:
- `POST /api/decisions/{id}/options` - Add option
- `PUT /api/decisions/{id}/options/{opt_id}` - Update option
- `DELETE /api/decisions/{id}/options/{opt_id}` - Delete option

**Criteria**:
- `POST /api/decisions/{id}/criteria` - Add criterion
- `PUT /api/decisions/{id}/criteria/{crit_id}` - Update criterion (name, weight)
- `DELETE /api/decisions/{id}/criteria/{crit_id}` - Delete criterion

**Scores**:
- `PUT /api/decisions/{id}/scores` - Bulk update scores
- Body: `[{ "option_id": 1, "criteria_id": 1, "score": 4 }, ...]`

**Export**:
- `GET /api/decisions/{id}/export?format=png` - Export as image

### Frontend

**Layout**:
- Left sidebar: Saved decisions list
- Main area: Active decision workspace
- Top: Decision title + options row
- Middle: Criteria × Options scoring grid
- Bottom: Results visualization

**Components**:

*Decision Header*:
- Editable title input
- Options as horizontal chips/tabs
- "Add Option" button
- Delete option (X) on hover

*Scoring Grid*:
- Rows = Criteria (with weight slider on left)
- Columns = Options
- Each cell = Score slider (1-5)
- Visual color coding based on score level
- Weight column shows importance (stars or bars)

*Criteria Row*:
- Drag handle for reordering
- Criterion name (editable)
- Weight slider (5 levels with labels)
- Score sliders for each option
- Delete button

*Results Panel*:
- Winner announcement with option name
- Horizontal bar chart showing weighted totals
- Score breakdown table (optional toggle)
- "Close call" or "Clear winner" indicator

*Sidebar*:
- Decision list with titles and dates
- Search/filter
- "New Decision" button
- Click to load decision

**Calculations**:
```
Weighted Score = Σ (criterion_weight × option_score) for all criteria
Winner = Option with highest weighted score
Score Gap = (Winner - Runner-up) / Winner × 100
```

**Chart Rendering**:
- Install `chart.js` for bar chart
- Horizontal bars, sorted by score descending
- Winner bar highlighted in green
- Animate on score changes

## Success Criteria

- [ ] Create decision with title
- [ ] Add 3+ options to compare
- [ ] Add 3+ criteria with weights
- [ ] Score each option against each criterion
- [ ] See real-time winner calculation
- [ ] Bar chart shows relative scores
- [ ] Save decision to library
- [ ] Load decision from library
- [ ] Duplicate decision for variations
- [ ] Export results as PNG
- [ ] Data persists after refresh

## Testing

### Manual Test Flow
1. Create "Choose a Database" decision
2. Add options: "PostgreSQL", "MongoDB", "SQLite"
3. Add criteria: "Performance", "Ease of Use", "Scalability", "Cost"
4. Set weights: Performance=Critical, Ease=Important, Scale=Very Important, Cost=Moderate
5. Score each option on each criterion
6. Verify winner updates as you adjust sliders
7. Save decision
8. Refresh page → decision still there
9. Duplicate → modify scores → see different winner
10. Export as PNG

### Validation
```bash
# List decisions
curl http://localhost:8000/api/decisions

# Create decision
curl -X POST http://localhost:8000/api/decisions \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Decision"}'

# Check database
sqlite3 decisions.db "SELECT * FROM decisions"
```

## Why This Works

- **Fast**: Sliders are faster than typing numbers or percentages
- **Visual**: See the winner instantly, understand the gap
- **Collaborative**: Easy to project on screen for team discussions
- **Revisable**: Duplicate and tweak weights to see "what if"
- **Exportable**: Share results with stakeholders

## UI Design

Build the "Clear Choice" theme interface with:
- Cool white background (#F8FAFC) for clarity
- Card-based layout with soft shadows
- Blue (#3B82F6) primary for actions
- Green (#10B981) for winner highlighting
- Score sliders with color-coded thumbs (red→green gradient)
- Prominent winner banner at top of results
- Horizontal bar chart with smooth animations
- Inter font throughout
- Responsive: grid collapses to accordion on mobile
- Loading states for save/load operations

**Build time: ~20 minutes**
