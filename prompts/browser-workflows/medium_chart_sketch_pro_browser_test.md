# Chart Sketch Pro - Visual Story Builder

## Browser UI Testing

### User Story Workflow 1: Create and Edit a Bar Chart
Validates that a user can create a new bar chart, add data points using sliders, and see real-time updates.

- [] Click "New Chart" button in the sidebar
- [] Select "Bar" chart type from the chart type selector
- [] Enter chart title "Q4 Sales Performance" in the title input
- [] Add a data point by clicking "Add Point" button
- [] Enter point name "Product A" and adjust the level slider to "High"
- [] Add another data point "Product B" with level "Medium"
- [] CONFIRM: Bar chart displays in canvas with two bars at different heights, title shows "Q4 Sales Performance"

### User Story Workflow 2: Switch Themes and Export Chart
Validates that a user can change the visual theme and export the chart as PNG.

- [] Open public URL with an existing chart
- [] Click on the theme picker in the properties panel
- [] Select "Corporate" theme from the options
- [] CONFIRM: Chart colors update to navy/steel blue palette
- [] Click "Export" button in the toolbar
- [] Select "PNG" from export options
- [] CONFIRM: PNG file downloads with the chart image

### User Story Workflow 3: Create Multi-Series Line Chart
Validates that a user can create a chart with multiple data series for comparison.

- [] Click "New Chart" and select "Line" chart type
- [] Enter title "Revenue Comparison"
- [] Add 3 data points: "Jan", "Feb", "Mar" with varying levels
- [] Click "Add Series" button to add a second series
- [] Name the second series "Last Year"
- [] Add matching data points for the second series
- [] CONFIRM: Two lines appear on the chart with different colors, legend shows both series names

### User Story Workflow 4: Create and Organize Collection
Validates that a user can create a collection and organize multiple charts within it.

- [] Click "New Collection" button in the sidebar
- [] Enter collection name "Q4 Report"
- [] Create a new Pie chart within the collection
- [] Add 4 data points representing market segments
- [] Click back to collection view in sidebar
- [] CONFIRM: Collection shows in sidebar with the pie chart nested under it, collection name displays as "Q4 Report"
