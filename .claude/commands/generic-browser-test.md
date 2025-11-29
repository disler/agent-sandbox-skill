---
model: opus
description: Execute browser UI testing workflows from a plan file against any URL
argument-hint: [url] [plan_file] [parallel:true|false] [headed:true|false]
---

# Purpose

Execute user story workflows defined in a plan file to validate UI functionality through browser automation against any public URL. Supports optional parallel execution of workflows using the Task tool.

## Variables

URL: $1
PLAN_FILE: $2
PARALLEL: $3 (default: false)
HEADED: $4 (default: false)
OUTPUT_DIR: `temp/generic-browser-test/`
BROWSER_CLI_PATH: `.claude/skills/agent-sandboxes/sandbox_cli/`

## Instructions

- CRITICAL: Re-read `PLAN_FILE` and locate a `Browser UI Testing` section or some equivalent section that defines the user story workflows to test.
- Execute ALL user story workflows from that section in order
- On ANY error, stop immediately, debug the issue, and report it
- Take screenshots on success and error states
- If `PARALLEL` is `true`, execute each workflow in a separate subagent using the Task tool
- If `PARALLEL` is `false` (default), execute workflows sequentially
- This command does NOT require a sandbox - it tests against any accessible URL
- ALWAYS run `uv run sbx browser --help` first to understand available browser commands
- Generate unique browser port for multi-agent safety
- If `HEADED` is `true`, start browser with `--headed` flag (visible window)
- If `HEADED` is `false` (default), run headless (no window)
- **CRITICAL - PORT ISOLATION**: Each agent/subagent MUST use its own unique port. NEVER close browsers on ports you didn't start.
- **CRITICAL - BROWSER CLOSE**: When closing browser, ALWAYS specify `--port $BROWSER_PORT`. This ensures you ONLY close YOUR browser, not other agents' browsers.

## Workflow

### 1. Setup

1. Change to `BROWSER_CLI_PATH` directory for all browser commands
2. Run `uv run sbx browser --help` to understand available commands and options
3. Re-read the plan file at `PLAN_FILE` and locate a `Browser UI Testing` section or some equivalent section that defines the user story workflows to test.
4. Extract all `User Story Workflow <N>: <Feature Name>` entries
5. Generate unique port for multi-agent safety:
   ```bash
   BROWSER_PORT=$((9222 + $RANDOM % 778))
   ```
6. Create output directory if needed: `mkdir -p temp/generic-browser-test/`

### 2. Determine Execution Mode

**If PARALLEL is false (default):**
- Proceed to Step 3 (Sequential Execution)

**If PARALLEL is true:**
- Skip to Step 4 (Parallel Execution)

### 3. Sequential Execution

1. Start browser:
   - If HEADED is true: `uv run sbx browser start --headed --port $BROWSER_PORT`
   - If HEADED is false: `uv run sbx browser start --port $BROWSER_PORT`
2. If Playwright is not installed:
   - `uv pip install playwright`
   - `uv run playwright install chromium`

For EACH `### User Story Workflow <N>: <Feature Name>` in the plan:

**Execute the workflow:**
- Navigate to URL: `uv run sbx browser nav [URL] --port $BROWSER_PORT`
- Execute each `- []` step using appropriate browser commands:
  - **Open URL**: `uv run sbx browser nav <url> --port $BROWSER_PORT`
  - **Click**: `uv run sbx browser click "<selector>" --port $BROWSER_PORT`
  - **Type/Fill**: `uv run sbx browser type "<selector>" "<text>" --port $BROWSER_PORT`
  - **Scroll**: `uv run sbx browser scroll <direction> --port $BROWSER_PORT`
  - **Evaluate JS**: `uv run sbx browser eval "<js code>" --port $BROWSER_PORT`
  - **Screenshot**: `uv run sbx browser screenshot --path <path> --port $BROWSER_PORT`
  - **Get DOM**: `uv run sbx browser dom --port $BROWSER_PORT`
  - **Get A11y Tree**: `uv run sbx browser a11y --port $BROWSER_PORT`
- **CONFIRM steps**: Verify expected outcome using `browser eval` or `browser screenshot`

**On ERROR:**
- Take error screenshot: `uv run sbx browser screenshot --path [OUTPUT_DIR]/<workflow-name>-error.png --port $BROWSER_PORT`
- Evaluate console for errors: `uv run sbx browser eval "JSON.stringify(window.consoleErrors || [])" --port $BROWSER_PORT`
- Document the exact step that failed
- Continue to next workflow (do not block other tests)

**On SUCCESS:**
- Take final screenshot: `uv run sbx browser screenshot --path [OUTPUT_DIR]/<workflow-name>-success.png --port $BROWSER_PORT`
- Mark workflow as PASSED

After all workflows complete:
- **CRITICAL**: Close ONLY your browser: `uv run sbx browser close --port $BROWSER_PORT`
- NEVER omit `--port` - this could kill other agents' browsers
- Skip to Step 5 (Report)

### 4. Parallel Execution (PARALLEL=true)

**CRITICAL - PORT ASSIGNMENT FOR PARALLEL MODE:**
- Assign DETERMINISTIC ports to each workflow based on index: `9222 + workflow_index`
- Workflow 1 gets port 9223, Workflow 2 gets port 9224, etc.
- This prevents port collisions when subagents start simultaneously
- DO NOT use `$RANDOM` in parallel mode - it causes collisions
- Validate each port is available before proceeding to the next workflow. If not, generate a new port and validate it again - repeat until you find an available port for every workflow.

For EACH `### User Story Workflow <N>: <Feature Name>` in the plan, launch a Task subagent:


Use the Task tool with subagent_type="general-purpose" for each workflow.

IMPORTANT: Assign each subagent a UNIQUE port based on workflow index:
- Workflow 1 → port 9223
- Workflow 2 → port 9224
- Workflow 3 → port 9225
- etc.

Prompt for each subagent (replace [ASSIGNED_PORT] with the deterministic port):

<subagent-prompt>
---
You are executing a browser UI test workflow.

**YOUR ASSIGNED PORT: [ASSIGNED_PORT]**

This port is exclusively yours. No other agent will use it.
You're operating on a SINGLE workflow. Do not work on any other workflows.

**Setup:**
1. cd to `.claude/skills/agent-sandboxes/sandbox_cli/`
2. Your port is: `BROWSER_PORT=[ASSIGNED_PORT]` (pre-validated by parent agent)
3. Start browser: `uv run sbx browser start [--headed if HEADED=true] --port $BROWSER_PORT`
4. Run `uv run sbx browser --help` to see all available commands and options you have for browser testing.
5. If Playwright not installed: `uv pip install playwright && uv run playwright install chromium`

**Headed Mode:** [HEADED value - true or false]

**Target URL:** [URL]

**Workflow to Execute:**
[Paste the full User Story Workflow N content from the plan here]

**Instructions:**
- Navigate to the URL first
- Execute each `- []` step in order using browser commands:
  - nav, click, type, scroll, eval, screenshot, dom, a11y
- For CONFIRM steps, verify using `browser eval` or `browser screenshot`
- On error: take screenshot to `temp/generic-browser-test/<workflow-name>-error.png`, document failure
- On success: take screenshot to `temp/generic-browser-test/<workflow-name>-success.png`

**CRITICAL - CLEANUP:**
- ONLY close YOUR browser on YOUR port: `uv run sbx browser close --port $BROWSER_PORT`
- NEVER run `sbx browser close` without `--port` - this may affect other agents
- NEVER close ports other than the one YOU started

**Return Format:**
```
Workflow: [Name]
Port Used: [ASSIGNED_PORT]
Status: PASSED or FAILED
Steps Executed: N of Total
Screenshot: [path]
Error Details: [if failed, describe what went wrong]
```
---
</subagent-prompt>

Launch ALL workflow subagents in a SINGLE message with multiple Task tool calls to execute in parallel.

Wait for all subagents to complete and collect their results.

### 5. Report

1. Generate filename based on plan file name: `<plan-name>_validation_results.md`
2. Save report to `[OUTPUT_DIR]/<filename>`
3. Return the report content to the user

Now follow the `Report` section to report the completed work.

## Report

Save to `temp/generic-browser-test/<plan-name>_validation_results.md` AND return to user:

```markdown
# Browser UI Testing Results

**URL Tested**: [URL]
**Plan File**: [PLAN_FILE]
**Execution Mode**: Sequential or Parallel
**Browser Mode**: Headless or Headed
**Timestamp**: [YYYY-MM-DD HH:MM:SS]

---

## Workflow Results

### User Story Workflow 1: [Feature Name]
- **Description**: [from plan]
- **Steps Executed**: [N] of [Total]
- **Screenshot**: [OUTPUT_DIR]/[workflow-name]-success.png
- **Status**: PASSED

### User Story Workflow 2: [Feature Name]
- **Description**: [from plan]
- **Steps Executed**: [N] of [Total]
- **Screenshot**: [OUTPUT_DIR]/[workflow-name]-success.png
- **Status**: PASSED

### User Story Workflow N: [Feature Name] (if failed)
- **Description**: [from plan]
- **Failed At Step**: [step number and description]
- **Error Screenshot**: [OUTPUT_DIR]/[workflow-name]-error.png
- **Error Details**: [what went wrong]
- **Status**: FAILED

---

## Summary

| Metric          | Value |
| --------------- | ----- |
| Total Workflows | [N]   |
| Passed          | [N]   |
| Failed          | [N]   |
| Pass Rate       | [X]%  |

**All Workflows Passed**: YES or NO

---

## Screenshots

| Workflow | Status | Screenshot |
| -------- | ------ | ---------- |
| [Name 1] | PASSED | [path]     |
| [Name 2] | PASSED | [path]     |
| [Name 3] | FAILED | [path]     |
```
