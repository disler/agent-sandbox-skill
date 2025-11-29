# Decision Matrix - Weighted Choice Visualizer

## Browser UI Testing

### User Story Workflow 1: Create Decision with Options
Validates that a user can create a new decision and add options to compare.

- [] Click "New Decision" button in sidebar
- [] Edit the decision title to "Choose a Database"
- [] Click "Add Option" and enter "PostgreSQL"
- [] Click "Add Option" and enter "MongoDB"
- [] Click "Add Option" and enter "SQLite"
- [] CONFIRM: Three options appear as chips in the header

### User Story Workflow 2: Add Criteria and Set Weights
Validates that a user can add criteria with different importance weights.

- [] Open public URL and select an existing decision
- [] Click "Add Criterion" button
- [] Enter criterion name "Performance"
- [] Adjust weight slider to level 5 (Critical)
- [] Add another criterion "Ease of Use" with weight 3
- [] Add criterion "Cost" with weight 2
- [] CONFIRM: Three criteria rows appear with correct weight indicators

### User Story Workflow 3: Score Options and See Results
Validates that scoring updates results in real-time.

- [] Open public URL and select a decision with options and criteria
- [] In the scoring grid, adjust score slider for first option/first criterion
- [] Adjust multiple score sliders across different cells
- [] Observe the results panel updating
- [] CONFIRM: Bar chart shows ranked options with winner highlighted in green

### User Story Workflow 4: Save and Load Decision
Validates that decisions persist and can be reloaded.

- [] Open public URL and create a decision with options, criteria, and scores
- [] Note the current winner shown in results
- [] Refresh the page
- [] Click on the decision in the sidebar to load it
- [] CONFIRM: All options, criteria, scores, and results are restored correctly
