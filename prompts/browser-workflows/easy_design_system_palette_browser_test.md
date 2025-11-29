# Design System Palette Generator

## Browser UI Testing

### User Story Workflow 1: Generate Color Palette
Validates that a user can enter a brand color and generate a harmonious palette.

- [] Locate the color picker/hex input field
- [] Enter brand color hex value: `#6366F1`
- [] Select "Triadic" harmony type button
- [] Wait for colors to generate
- [] CONFIRM: Three harmonious color swatches are displayed

### User Story Workflow 2: Preview Components with Palette
Validates that the generated palette is applied to UI component previews.

- [] Open public URL (palette should already be generated from workflow 1)
- [] Click on "Buttons" preview tab
- [] Observe button styles using palette colors
- [] Click on "Cards" preview tab
- [] Observe card styles using palette colors
- [] Toggle dark mode switch
- [] CONFIRM: Components update to dark mode styling with palette colors

### User Story Workflow 3: Save and Load Palette
Validates that a user can save a palette and load it from the library.

- [] Open public URL with a generated palette
- [] Click "Save Palette" button
- [] Enter palette name: "My Indigo Theme"
- [] Click confirm/save
- [] Observe palette appears in library sidebar
- [] CONFIRM: Palette is saved and visible in the library list

### User Story Workflow 4: Export Palette as CSS
Validates that a user can export the palette in CSS format.

- [] Open public URL with a saved palette
- [] Locate the Export panel
- [] Click "CSS" format tab
- [] Observe CSS variables code in preview
- [] Click "Copy" button
- [] CONFIRM: CSS variables are displayed with proper format (--color-primary-500: #...)
