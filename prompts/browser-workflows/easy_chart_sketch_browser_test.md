# Chart Sketch - Visual Idea Communicator

## Browser UI Testing

### User Story Workflow 1: Create Bar Chart with Sliders
Validates that a user can create a bar chart and adjust data point levels using sliders.

- [] Verify default bar chart canvas is displayed
- [] Enter chart title "Team Priorities" in the title input
- [] Add a new data point by clicking "Add Point" button
- [] Adjust the slider for the first data point to "High" level
- [] CONFIRM: Bar chart updates in real-time showing the adjusted bar height

### User Story Workflow 2: Switch Chart Types
Validates that a user can switch between bar, pie, and line chart types.

- [] Create a chart with at least 3 data points
- [] Click on the "Pie" chart type icon
- [] CONFIRM: Chart re-renders as a pie chart with correct proportions
- [] Click on the "Line" chart type icon
- [] CONFIRM: Chart re-renders as a line chart connecting the data points

### User Story Workflow 3: Save and Load Chart
Validates that a user can save a chart and load it from the library.

- [] Create a chart with title "Q4 Goals" and 3 data points
- [] Click "Save" button to save the chart
- [] CONFIRM: Chart appears in the library sidebar
- [] Create a new chart (or modify current one)
- [] Click on the saved "Q4 Goals" chart in the library
- [] CONFIRM: Chart loads with original title and data points restored

### User Story Workflow 4: Export Chart as PNG
Validates that a user can download their chart as a PNG image.

- [] Create a chart with title and data points
- [] Click "Download PNG" button
- [] CONFIRM: PNG file downloads (check browser download or verify button triggers download)

### User Story Workflow 5: Export Chart as SVG
Validates that a user can download their chart as an SVG vector image.

- [] Create a chart with title "Vector Export Test" and at least 2 data points
- [] Click "SVG" button in the header
- [] CONFIRM: SVG file downloads (verify button triggers download action)

### User Story Workflow 6: Delete Chart from Library
Validates that a user can remove a saved chart from the library.

- [] Create and save a chart with title "Delete Me"
- [] CONFIRM: Chart appears in the library sidebar
- [] Click the delete button (🗑️) next to the "Delete Me" chart
- [] CONFIRM: Chart is removed from the library sidebar

### User Story Workflow 7: Customize Axis Labels
Validates that a user can set custom labels for X and Y axes.

- [] Create a new chart or use existing one
- [] Enter "Categories" in the X-AXIS LABEL input
- [] Enter "Priority Level" in the Y-AXIS LABEL input
- [] CONFIRM: Axis labels are displayed on the chart canvas

### User Story Workflow 8: Remove Data Points
Validates that a user can remove individual data points from the chart.

- [] Start with a chart that has 3 or more data points
- [] Click the remove button (×) on the second data point
- [] CONFIRM: Data point is removed and chart updates to show only remaining points
- [] CONFIRM: Chart re-renders correctly with updated data
