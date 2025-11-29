# Browser Automation Cookbook

Visual validation tools for sandbox applications using Playwright's isolated Chromium.

## Quick Start

```bash
cd .claude/skills/agent-sandboxes/sandbox_cli

# 1. Initialize (first time only)
uv run sbx browser init

# 2. Start browser
uv run sbx browser start

# 3. Navigate
uv run sbx browser nav https://example.com

# 4. Interact / Validate
uv run sbx browser eval "document.title"
uv run sbx browser screenshot --path screenshot.png

# 5. Close when done
uv run sbx browser close
```

## Commands Reference

```bash
uv run sbx browser <subcommand> [options]

Subcommands:
  init                Initialize browser environment (run once per machine)
  start               Start Playwright Chromium with remote debugging
  nav URL             Navigate to a URL
  screenshot          Take a screenshot of the current page
  eval CODE           Execute JavaScript in the page
  click SELECTOR      Click an element
  type SELECTOR TEXT  Type text into an input field
  press KEY           Press a keyboard key
  scroll DIRECTION    Scroll the page (up/down/top/bottom)
  a11y                Get accessibility tree snapshot
  dom                 Get DOM structure (simplified or full)
  pick MESSAGE        Interactive element picker
  cookies             Get all cookies as JSON
  status              Check browser connection status
  close               Close the browser and terminate process
```

## First-Time Setup

Run once per machine to install Playwright and Chromium:

```bash
uv run sbx browser init
```

This is idempotent - safe to run multiple times.

## Headless vs Headed Mode

```bash
# Headless (default) - no window, runs in background
uv run sbx browser start

# Headed - shows visible browser window (useful for debugging)
uv run sbx browser start --headed
```

## Multi-Agent Parallel Execution

Multiple agents can run browsers simultaneously using different ports:

```bash
# Agent 1: uses default port 9222
uv run sbx browser start
uv run sbx browser nav https://app1.example.com

# Agent 2: uses port 9223
uv run sbx browser start --port 9223
uv run sbx browser nav https://app2.example.com --port 9223

# Agent 3: uses port 9224
uv run sbx browser start --port 9224
uv run sbx browser nav https://app3.example.com --port 9224
```

**IMPORTANT for parallel agents**:
1. Generate a unique port (e.g., `9222 + RANDOM % 778`)
2. Use `--port` flag consistently on ALL browser commands
3. Close your own browser when done: `sbx browser close --port <port>`

## Common Patterns

### Check Page Loads
```bash
uv run sbx browser nav <url>
uv run sbx browser eval "document.readyState"
```

### Verify UI Elements
```bash
uv run sbx browser eval "document.querySelectorAll('button').length"
uv run sbx browser eval "document.querySelector('h1')?.textContent"
```

### Extract Data
```bash
# Get all link texts
uv run sbx browser eval "Array.from(document.querySelectorAll('a')).map(a => a.textContent)"

# Get structured data
uv run sbx browser eval "Array.from(document.querySelectorAll('.item')).map(el => ({title: el.querySelector('h2')?.textContent, price: el.querySelector('.price')?.textContent}))"
```

### Interact with Forms
```bash
uv run sbx browser type "#username" "testuser"
uv run sbx browser type "#password" "testpass"
uv run sbx browser click "#submit-button"
```

### Keyboard Navigation
```bash
uv run sbx browser press Tab
uv run sbx browser press Enter
uv run sbx browser press Escape
```

### Scroll Page
```bash
uv run sbx browser scroll down
uv run sbx browser scroll down --amount 1000
uv run sbx browser scroll top
uv run sbx browser scroll bottom
```

### Screenshots
```bash
# Viewport only
uv run sbx browser screenshot --path screenshot.png

# Full page
uv run sbx browser screenshot --full --path full-page.png
```

### Get Page Structure
```bash
# Simplified DOM (good for LLMs)
uv run sbx browser dom

# Full HTML
uv run sbx browser dom --full

# Accessibility tree (best for understanding page structure)
uv run sbx browser a11y
```

## Validating Sandbox Applications

When testing web apps hosted in E2B sandboxes:

```bash
# 1. Get the public URL from sandbox
uv run sbx sandbox get-host <sandbox_id> --port 5173
# Returns: https://5173-<sandbox_id>.e2b.app

# 2. Start browser and navigate
uv run sbx browser start
uv run sbx browser nav https://5173-<sandbox_id>.e2b.app

# 3. Validate
uv run sbx browser eval "document.readyState"
uv run sbx browser screenshot --path validation.png

# 4. Close
uv run sbx browser close
```

## Troubleshooting

### "Browser environment not initialized"
```bash
uv run sbx browser init
```

### "Could not connect to Chromium on port XXXX"
```bash
# Start the browser first
uv run sbx browser start --port XXXX
```

### "Port XXXX is already in use"
```bash
# Option 1: Use different port
uv run sbx browser start --port 9223

# Option 2: Close existing browser
uv run sbx browser close --port 9222

# Option 3: Check what's using the port
lsof -i :9222
```

### "Failed to start browser"
```bash
# 1. Re-run init
uv run sbx browser init

# 2. Kill stale processes
pkill -f "chromium.*remote-debugging"

# 3. Try different port
uv run sbx browser start --port 9223
```

### Multiple agents failing
Each agent MUST use a unique port:
```bash
BROWSER_PORT=$((9222 + RANDOM % 778))
uv run sbx browser start --port $BROWSER_PORT
# Use --port $BROWSER_PORT on ALL subsequent commands
```

## Important Notes

- Browser commands run on YOUR local machine, not in the sandbox
- Uses **Playwright's isolated Chromium** - does NOT interfere with your Chrome browser
- Runs in **headless mode by default** - no browser window appears
- The browser persists across commands until you `close` it
- Use `get-host` to get sandbox URLs, then validate with browser commands
