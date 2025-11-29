---
description: Execute browser UI testing workflows from a plan file against a running application
argument-hint: [sandbox_id] [public_url] [plan_file_path] [workflow_id]
---

# Browser UI Testing

Execute user story workflows defined in a plan file to validate UI functionality through browser automation. Supports parallel execution via subagents.

## Variables

SANDBOX_ID: $1
PUBLIC_URL: $2
PLAN_FILE_PATH: $3
WORKFLOW_ID: $4
BROWSER_UI_TESTING_SCREENSHOT_PATH: `temp/<WORKFLOW_ID>/ui-testing/`
SANDBOX_CLI_PATH: `.claude/skills/agent-sandboxes/sandbox_cli/`
USE_SUBAGENTS: true (static default)
HEADLESS: true (static default)

## Instructions

- CRITICAL: Re-read `PLAN_FILE_PATH` and locate the `### 7. Browser UI Testing` section
- Extract ALL user story workflows from that section
- If `USE_SUBAGENTS` is true, execute workflows in parallel using Task tool
- If `USE_SUBAGENTS` is false, execute workflows sequentially
- If `HEADLESS` is false, start browsers with `--headed` flag (visible window)
- If `HEADLESS` is true, start browsers WITHOUT `--headed` flag
- **CRITICAL - PORT ISOLATION**: Each subagent MUST use its own unique port
- **CRITICAL - BROWSER CLOSE**: Always specify `--port` when closing browsers

## Workflow

### 1. Setup (Primary Agent)

1. Change to `SANDBOX_CLI_PATH` directory
2. Run `uv run sbx browser --help` to understand available commands
3. Re-read plan file at `PLAN_FILE_PATH` and locate `### 7. Browser UI Testing` section
4. Extract all `### User Story Workflow <N>: <Feature Name>` entries
5. Count total workflows (N)
6. Create output directory: `mkdir -p [BROWSER_UI_TESTING_SCREENSHOT_PATH]`

### 2. Port Validation (Primary Agent)

Assign and validate ports BEFORE launching subagents:

```bash
# Assign deterministic ports based on workflow index
# Workflow 1 → port 9223
# Workflow 2 → port 9224
# Workflow 3 → port 9225
# etc.

# Validate each port is available
for port in 9223 9224 9225 ...; do
  lsof -i :$port 2>/dev/null && echo "Port $port: IN USE" || echo "Port $port: AVAILABLE"
done
```

If a port is in use, increment until an available port is found for each workflow.

### 3. Execute Workflows

**If USE_SUBAGENTS is true (default):**

Launch ALL workflow subagents in a SINGLE message with multiple Task tool calls.

For EACH workflow, use Task tool with `subagent_type="general-purpose"`:

<subagent-prompt>
You are executing a browser UI test workflow.

**YOUR ASSIGNED PORT: [ASSIGNED_PORT]**

This port is exclusively yours. No other agent will use it.
You're operating on a SINGLE workflow. Do not work on any other workflows.

**Setup:**
1. cd to `[SANDBOX_CLI_PATH]`
2. Your port is: `BROWSER_PORT=[ASSIGNED_PORT]` (pre-validated by parent agent)
3. Start browser: `uv run sbx browser start [--headed if HEADLESS=false] --port $BROWSER_PORT`
4. Run `uv run sbx browser --help` to see all available commands and options
5. If Playwright not installed: `uv pip install playwright && uv run playwright install chromium`

**Headed Mode:** [true if HEADLESS=false, false if HEADLESS=true]

**Target URL:** [PUBLIC_URL]

**Workflow to Execute:**
[Paste the full User Story Workflow N content from the plan here]

**Instructions:**
- Navigate to the URL first: `uv run sbx browser nav [PUBLIC_URL] --port $BROWSER_PORT`
- Execute each `- []` step in order using browser commands:
  - **nav**: Navigate to URL
  - **click**: Click element by selector
  - **type**: Type text into input
  - **scroll**: Scroll page (up/down/top/bottom)
  - **eval**: Execute JavaScript
  - **screenshot**: Take screenshot
  - **dom**: Get DOM structure
  - **a11y**: Get accessibility tree
- For CONFIRM steps, verify using `browser eval` or `browser screenshot`
- On error: take screenshot to `[BROWSER_UI_TESTING_SCREENSHOT_PATH]/[workflow-name]-error.png`
- On success: take screenshot to `[BROWSER_UI_TESTING_SCREENSHOT_PATH]/[workflow-name]-success.png`

**CRITICAL - CLEANUP:**
- ONLY close YOUR browser on YOUR port: `uv run sbx browser close --port [ASSIGNED_PORT]`
- NEVER run `sbx browser close` without `--port`
- NEVER close ports other than [ASSIGNED_PORT]

**Return this exact format:**
```
Workflow: [Name]
Port Used: [ASSIGNED_PORT]
Status: PASSED or FAILED
Steps Executed: [N] of [Total]
Screenshot: [path to success or error screenshot]
Error Details: [if failed, describe what went wrong]
```
</subagent-prompt>

Wait for all subagents to complete and collect their results.

**If USE_SUBAGENTS is false:**

Execute workflows sequentially (see Sequential Execution section below).

### 4. Sequential Execution (If USE_SUBAGENTS=false)

1. Generate unique port:
   ```bash
   BROWSER_PORT=$((9222 + $(echo -n "[SANDBOX_ID]" | cksum | cut -d' ' -f1) % 778))
   ```
2. Start browser:
   - If HEADLESS=false: `uv run sbx browser start --headed --port $BROWSER_PORT`
   - If HEADLESS=true: `uv run sbx browser start --port $BROWSER_PORT`

For EACH workflow:
- Navigate to URL: `uv run sbx browser nav [PUBLIC_URL] --port $BROWSER_PORT`
- Execute each step using browser commands
- On ERROR: screenshot, debug, fix, re-run workflow from beginning
- On SUCCESS: screenshot, proceed to next workflow

After all workflows:
- Close browser: `uv run sbx browser close --port $BROWSER_PORT`

### 5. Collect Results (Primary Agent)

After all workflows complete (parallel or sequential):
1. Collect status from each workflow
2. Count passed/failed
3. Generate final report

## Report

The primary agent produces the final report after collecting all subagent results.

Save to `temp/<WORKFLOW_ID>/app_review/<plan-name>-browser-testing-<hhmmss>.md` AND return to user:

```markdown
# Browser UI Testing Results

**Sandbox ID**: [SANDBOX_ID]
**Public URL**: [PUBLIC_URL]
**Plan File**: [PLAN_FILE_PATH]
**Workflow ID**: [WORKFLOW_ID]
**Execution Mode**: Parallel (subagents) or Sequential
**Browser Mode**: Headed or Headless
**Timestamp**: [YYYY-MM-DD HH:MM:SS]

---

## Workflow Results

### User Story Workflow 1: [Feature Name]
- **Description**: [from plan]
- **Port Used**: [port number]
- **Steps Executed**: [N] of [Total]
- **Screenshot**: [BROWSER_UI_TESTING_SCREENSHOT_PATH]/[workflow-name]-success.png
- **Status**: PASSED

### User Story Workflow 2: [Feature Name]
- **Description**: [from plan]
- **Port Used**: [port number]
- **Steps Executed**: [N] of [Total]
- **Screenshot**: [BROWSER_UI_TESTING_SCREENSHOT_PATH]/[workflow-name]-success.png
- **Status**: PASSED

### User Story Workflow N: [Feature Name] (if failed)
- **Description**: [from plan]
- **Port Used**: [port number]
- **Failed At Step**: [step number and description]
- **Error Screenshot**: [BROWSER_UI_TESTING_SCREENSHOT_PATH]/[workflow-name]-error.png
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

| Workflow | Port | Status | Screenshot |
| -------- | ---- | ------ | ---------- |
| [Name 1] | 9223 | PASSED | [path]     |
| [Name 2] | 9224 | PASSED | [path]     |
| [Name 3] | 9225 | FAILED | [path]     |
```
