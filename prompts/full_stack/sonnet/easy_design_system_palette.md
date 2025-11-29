# Design System Palette - Theme & Component Builder

Build a color palette studio focused on creating complete design systems for applications. Generate harmonious color schemes, preview them on real UI components, and export production-ready CSS, Tailwind configs, and design tokens.

## Value Proposition

Stop guessing at colors. Start with one brand color and generate a complete, accessible design system in minutes. Preview your palette on actual buttons, cards, and forms - not just color swatches. Export directly to your codebase.

## Core Features

### Palette Generation
- **Brand Color Input**: Enter a hex color or use color picker
- **Auto-Generate Harmonies**:
  - Complementary (opposite on color wheel)
  - Analogous (adjacent colors)
  - Triadic (three evenly spaced)
  - Split-Complementary (Y-shape)
  - Monochromatic (shades of one hue)
- **Shade Generation**: Auto-create 50-950 scale for each color (like Tailwind)
- **One-click regenerate** with variations

### Semantic Color Mapping
- Map generated colors to semantic roles:
  - **Primary**: Main brand/action color
  - **Secondary**: Supporting color
  - **Accent**: Highlights and emphasis
  - **Success**: Positive actions/states (#green family)
  - **Warning**: Caution states (#amber family)
  - **Error**: Destructive/error states (#red family)
  - **Neutral**: Text, backgrounds, borders (auto-generated grays)
- Drag-and-drop to reassign colors to roles

### Live Component Preview
- See your palette applied to real UI components:
  - **Buttons**: Primary, secondary, outline, ghost, destructive
  - **Cards**: With headers, content, footers
  - **Forms**: Inputs, selects, checkboxes, toggles
  - **Alerts**: Success, warning, error, info
  - **Badges**: Various colors and styles
  - **Navigation**: Header, sidebar, tabs
- Toggle light/dark mode preview
- Mobile and desktop viewport previews

### Accessibility Checker
- WCAG contrast ratio for text on backgrounds
- Pass/fail indicators (AA, AAA levels)
- Suggested fixes for failing combinations
- Color blindness simulation (protanopia, deuteranopia, tritanopia)

### Save & Organize
- Save palettes to library with names
- Tag palettes (e.g., "SaaS", "E-commerce", "Dashboard")
- Duplicate and iterate on palettes
- Version history (last 3 versions)

### Export Options
- **CSS Variables**: Complete :root declaration
- **Tailwind Config**: tailwind.config.js colors section
- **Design Tokens**: JSON format for design tools
- **SCSS Variables**: $variable format
- **Figma-ready**: Copy individual colors
- **Full theme file**: All formats in one download

## UI Theme: "Studio Light"

A neutral, tool-focused interface that doesn't compete with the colors being designed.

### Color Palette (Meta - the app's own theme)
- **Background**: True neutral (#F5F5F5)
- **Surface**: White (#FFFFFF)
- **Workspace**: Light gray (#FAFAFA)
- **Border**: Medium gray (#E0E0E0)
- **Text Primary**: Near black (#212121)
- **Text Secondary**: Dark gray (#616161)
- **Text Muted**: Medium gray (#9E9E9E)
- **Interactive**: Neutral blue (#2563EB) - unobtrusive
- **Focus Ring**: Blue with low opacity

### Typography
- **Font Family**: Inter (UI), JetBrains Mono (code/hex values)
- **Section Headers**: 16px, Semi-bold
- **Labels**: 13px, Medium
- **Hex Values**: 14px, Mono, uppercase
- **Code Blocks**: 13px, Mono

### Styling
- Minimal shadows (0 1px 2px rgba(0,0,0,0.05))
- Subtle borders (1px solid #E0E0E0)
- Small radius (4px) - tool-like, not playful
- Color swatches: 48px circles or 64px squares
- Checkerboard background for transparency indication
- Generous whitespace for color breathing room

## Technical Requirements

### Database Schema

**Palettes**:
- id (primary key)
- name (text)
- brand_color (text: hex)
- harmony_type (text: complementary, analogous, etc.)
- tags (text: comma-separated)
- created_at (timestamp)
- updated_at (timestamp)

**PaletteColors**:
- id (primary key)
- palette_id (foreign key)
- role (text: primary, secondary, accent, success, warning, error, neutral)
- base_hex (text: the main color)
- shades (json: {"50": "#...", "100": "#...", ..., "950": "#..."})

**PaletteVersions**:
- id (primary key)
- palette_id (foreign key)
- snapshot (json: full palette state)
- created_at (timestamp)

### Backend API

**Palettes**:
- `GET /api/palettes` - List all palettes
- `GET /api/palettes/{id}` - Get palette with colors
- `POST /api/palettes` - Create palette
- `PUT /api/palettes/{id}` - Update palette
- `DELETE /api/palettes/{id}` - Delete palette
- `POST /api/palettes/{id}/duplicate` - Duplicate palette

**Generation**:
- `POST /api/generate/harmony` - Generate harmony from brand color
  - Body: `{ "brand_color": "#3B82F6", "harmony_type": "complementary" }`
  - Returns: Array of generated hex colors
- `POST /api/generate/shades` - Generate shade scale
  - Body: `{ "base_color": "#3B82F6" }`
  - Returns: `{ "50": "#...", "100": "#...", ..., "950": "#..." }`
- `POST /api/generate/neutrals` - Generate neutral gray scale
  - Body: `{ "brand_color": "#3B82F6" }` (tints grays toward brand)
  - Returns: Neutral shade scale with subtle brand tint

**Accessibility**:
- `POST /api/accessibility/contrast` - Check contrast ratio
  - Body: `{ "foreground": "#FFFFFF", "background": "#3B82F6" }`
  - Returns: `{ "ratio": 4.5, "aa_normal": true, "aa_large": true, "aaa_normal": false }`

**Export**:
- `GET /api/palettes/{id}/export?format=css` - CSS variables
- `GET /api/palettes/{id}/export?format=tailwind` - Tailwind config
- `GET /api/palettes/{id}/export?format=tokens` - Design tokens JSON
- `GET /api/palettes/{id}/export?format=scss` - SCSS variables

### Frontend

**Layout**:
- Left panel: Palette library (saved palettes)
- Center: Main workspace (generation + preview)
- Right panel: Export options + accessibility

**Workspace Sections**:

*Brand Color Input*:
- Large color picker (native + custom)
- Hex input field with validation
- Recent colors row
- "Randomize" button for inspiration

*Harmony Generator*:
- Harmony type selector (5 options as icon buttons)
- Generated colors as large swatches
- Click swatch to see shade scale
- "Regenerate" button for variations
- Drag colors to semantic role slots

*Semantic Role Mapping*:
- Drop zones for: Primary, Secondary, Accent
- Auto-assigned: Success (green), Warning (amber), Error (red)
- Neutral scale (auto-generated from brand)
- Each role shows base color + shade preview

*Component Preview*:
- Tab bar: Buttons | Cards | Forms | Alerts | Navigation
- Light/Dark mode toggle
- Viewport size toggle (mobile/desktop)
- Live-updating components using palette CSS variables

*Accessibility Panel*:
- Contrast grid showing all text/background combinations
- Green checkmarks / red X for pass/fail
- Color blindness simulation dropdown
- "Fix suggestions" for failing combinations

*Export Panel*:
- Format selector tabs
- Code preview with syntax highlighting
- "Copy" button for each format
- "Download All" for zip of all formats

**Color Algorithms** (implement in backend):
```python
# Harmony generation using HSL color space
def complementary(hsl): return rotate_hue(hsl, 180)
def analogous(hsl): return [rotate_hue(hsl, -30), hsl, rotate_hue(hsl, 30)]
def triadic(hsl): return [hsl, rotate_hue(hsl, 120), rotate_hue(hsl, 240)]

# Shade generation
def generate_shades(hex_color):
    # Convert to HSL, vary lightness from 97% (50) to 10% (950)
    # Maintain hue, slightly reduce saturation at extremes
```

## Success Criteria

- [ ] Enter brand color via picker or hex input
- [ ] Generate harmonious palette (5 harmony types work)
- [ ] See shade scales (50-950) for each color
- [ ] Map colors to semantic roles (drag-and-drop)
- [ ] Preview on button components
- [ ] Preview on card components
- [ ] Preview on form components
- [ ] Toggle light/dark mode preview
- [ ] See accessibility contrast checks
- [ ] Export as CSS variables
- [ ] Export as Tailwind config
- [ ] Save palette to library
- [ ] Load palette from library

## Testing

### Manual Test Flow
1. Open app → empty workspace with color picker
2. Enter brand color: #6366F1 (indigo)
3. Select "Triadic" harmony → see 3 colors generated
4. View shade scale for primary color
5. Drag secondary color to "Accent" role
6. Switch to "Buttons" preview tab → see styled buttons
7. Toggle dark mode → buttons adapt
8. Check accessibility panel → verify contrast ratios
9. Export as CSS → copy variables
10. Export as Tailwind → valid config object
11. Save palette as "Indigo SaaS Theme"
12. Refresh → palette in library

### Validation
```bash
# Generate harmony
curl -X POST http://localhost:8000/api/generate/harmony \
  -H "Content-Type: application/json" \
  -d '{"brand_color":"#6366F1","harmony_type":"triadic"}'

# Check contrast
curl -X POST http://localhost:8000/api/accessibility/contrast \
  -H "Content-Type: application/json" \
  -d '{"foreground":"#FFFFFF","background":"#6366F1"}'

# Export CSS
curl http://localhost:8000/api/palettes/1/export?format=css
```

## Export Format Examples

### CSS Variables
```css
:root {
  --color-primary-50: #EEF2FF;
  --color-primary-100: #E0E7FF;
  --color-primary-500: #6366F1;
  --color-primary-900: #312E81;

  --color-secondary-500: #F1F163;
  --color-accent-500: #63F1E0;

  --color-success-500: #10B981;
  --color-warning-500: #F59E0B;
  --color-error-500: #EF4444;

  --color-neutral-50: #F9FAFB;
  --color-neutral-900: #111827;
}
```

### Tailwind Config
```javascript
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#EEF2FF',
          500: '#6366F1',
          900: '#312E81',
        },
        // ... other colors
      }
    }
  }
}
```

## Why This Works

- **One input, full output**: Enter one color, get complete design system
- **Real previews**: See actual components, not abstract swatches
- **Accessible by default**: Catch contrast issues before shipping
- **Production-ready**: Export directly to your stack
- **Iterate fast**: Save, duplicate, compare variations

## UI Design

Build the "Studio Light" theme interface with:
- Neutral gray background (#F5F5F5) that doesn't influence color perception
- Clean white panels with subtle 1px borders
- Generous spacing around color swatches
- JetBrains Mono for hex values and code
- Large, clickable color swatches (48-64px)
- Tab-based navigation for preview components
- Split-pane layout: palette generation left, preview right
- Sticky export panel
- Smooth transitions on color changes
- Loading states for generation operations

**Build time: ~25 minutes**
