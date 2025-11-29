---
model: claude-sonnet-4-5-20250929
description: Execute browser automation tasks against a URL using Playwright
argument-hint: [url] [prompt]
---

# Purpose

Execute browser automation and validation tasks against a URL using Playwright Chromium. Supports navigation, screenshots, JavaScript evaluation, and visual inspection based on a user-provided prompt.

## Variables

URL: $1
USER_PROMPT: $2

## Instructions

- **IMPORTANT**: Change to `.claude/skills/agent-sandboxes/sandbox_cli/` directory for all browser commands
- Generate a unique browser port to avoid conflicts with parallel agents
- All browser commands MUST include `--port $BROWSER_PORT`
- Browser runs in headless mode by default (no window appears)
- Always close the browser when done

## Workflow

### Step 1: Setup Working Directory

```bash
cd .claude/skills/agent-sandboxes/sandbox_cli
```

### Step 2: Generate Unique Port

Generate a unique port for this browser session to avoid conflicts with parallel agents:

```bash
BROWSER_PORT=$((9222 + RANDOM % 778))
echo "Using port: $BROWSER_PORT"
```

### Step 3: Start Browser

Start the browser. If this fails with "Browser environment not initialized", run init first.

```bash
uv run sbx browser start --port $BROWSER_PORT
```

**If start fails with initialization error**:
```bash
# Run init to install Playwright and Chromium (one-time setup)
uv run sbx browser init

# Then retry start
uv run sbx browser start --port $BROWSER_PORT
```

**If start fails with "port in use"**:
```bash
# Try a different port
BROWSER_PORT=$((9223 + RANDOM % 777))
uv run sbx browser start --port $BROWSER_PORT
```

### Step 4: Navigate to URL

```bash
uv run sbx browser nav [URL] --port $BROWSER_PORT
```

### Step 5: Execute User's Prompt

Use available browser commands to fulfill the user's request:

**Get page information**:
```bash
uv run sbx browser eval "document.title" --port $BROWSER_PORT
uv run sbx browser eval "document.readyState" --port $BROWSER_PORT
```

**Query elements**:
```bash
uv run sbx browser eval "document.querySelector('...')?.textContent" --port $BROWSER_PORT
uv run sbx browser eval "document.querySelectorAll('...').length" --port $BROWSER_PORT
uv run sbx browser eval "Array.from(document.querySelectorAll('...')).map(el => el.textContent)" --port $BROWSER_PORT
```

**Take screenshots**:
```bash
uv run sbx browser screenshot --path /tmp/screenshot.png --port $BROWSER_PORT
uv run sbx browser screenshot --full --path /tmp/full-page.png --port $BROWSER_PORT
```

**Interact with page**:
```bash
uv run sbx browser click "#button-id" --port $BROWSER_PORT
uv run sbx browser type "#input-id" "text to type" --port $BROWSER_PORT
uv run sbx browser scroll down --port $BROWSER_PORT
```

**Get structured data**:
```bash
uv run sbx browser a11y --port $BROWSER_PORT  # Accessibility tree
uv run sbx browser dom --port $BROWSER_PORT   # Simplified DOM
```

### Step 6: Close Browser

Always close the browser when done:

```bash
uv run sbx browser close --port $BROWSER_PORT
```

### Step 7: Report Results

Present results using the format below.

## Report

```markdown
# Browser Task Results

**URL**: [URL]
**Task**: [USER_PROMPT]

---

## Findings

[Summary of what was discovered or accomplished based on the user's prompt]

## Evidence

- **Page Title**: [title from browser eval]
- **Screenshot**: [path if taken]
- **Key Elements**: [relevant findings from JS evaluation]

---

**Status**: [COMPLETED / FAILED with reason]
```

## Error Handling

| Error | Solution |
|-------|----------|
| "Browser environment not initialized" | Run `uv run sbx browser init` then retry |
| "Port XXXX is already in use" | Use different port: `--port $((9223 + RANDOM % 777))` |
| "Could not connect to Chromium" | Run `uv run sbx browser start --port $BROWSER_PORT` |
| "Failed to start browser" | Run init, check for stale processes: `pkill -f chromium.*remote-debugging` |
