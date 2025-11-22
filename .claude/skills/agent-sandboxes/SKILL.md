---
name: Agent Sandboxes
description: Operate E2B agent sandboxes using the CLI. Use when user needs to run code in isolation, test packages, execute commands safely, or work with binary files in a sandbox environment. Keywords: sandbox, e2b, isolated environment, run code, test code, safe execution.
---

# Agent Sandboxes

This skill provides access to E2B sandboxes through a streamlined CLI for safe code execution and file operations in isolated environments.

## Variables

- **E2B API Key**: Required environment variable `E2B_API_KEY`
- **Sandbox CLI Location**: `.claude/skills/agent-sandboxes/sandbox_cli/`
- **Environment File**: Root `.env` file (automatically loaded)

## Prerequisites

Before using sandbox operations, **validate the environment**:

1. **Check for E2B_API_KEY**:
   ```bash
   # Verify the API key is set
   grep "E2B_API_KEY" .env
   ```

   If missing, instruct the user:
   ```
   Error: E2B_API_KEY not found in .env file

   Please add your E2B API key to the .env file in the project root:
   echo "E2B_API_KEY=your_api_key_here" >> .env

   Get your API key from: https://e2b.dev/docs
   ```

2. **Verify CLI is available**:
   The sandbox CLI is located at `.claude/skills/agent-sandboxes/sandbox_cli/`
   The `.env` file is automatically loaded from the project root.

## Instructions

- IMPORTANT: Don't create files locally, always use the sandbox. Only do this if the user explicitly asks you to do so.

### When to Use Sandboxes

Use agent sandboxes when the user needs to:
- **Run untrusted or experimental code** safely
- **Test packages or dependencies** without affecting the local system
- **Execute system commands** in an isolated environment
- **Work with binary files** (images, PDFs, executables)
- **Clone and test repositories** in isolation
- **Install and test different package versions**
- **Run long-running processes** without blocking

### CLI Overview

The sandbox CLI has **four core command groups**:

1. **`sbx init`** - Quick sandbox initialization
2. **`sbx sandbox`** - Lifecycle management (create, connect, kill, pause, info)
3. **`sbx files`** - File operations (ls, read, write, upload, download, rm, mkdir, mv)
4. **`sbx exec`** - Unified command execution (the most powerful command)
5. **`sbx browser`** - Browser automation for UI validation (visual testing)

**Get CLI Help**: Use `sbx --help` to see all available commands and options:
```bash
cd .claude/skills/agent-sandboxes/sandbox_cli
uv run sbx --help           # Main help
uv run sbx init --help      # Help for init command
uv run sbx sandbox --help   # Help for sandbox commands
uv run sbx files --help     # Help for file operations
uv run sbx exec --help      # Help for exec command
```

### Key Command: `sbx exec`

The `exec` command is the primary interface for running commands in sandboxes:

```bash
uv run sbx exec $SANDBOX_ID "command" [options]

Options:
  --cwd PATH          Working directory
  --env KEY=VALUE     Environment variables (multiple allowed)
  --root              Run as root user
  --shell             Enable shell features (pipes, redirections, wildcards)
  --timeout SECONDS   Command timeout (default: 60)
  --background        Run command in background
```

**Important**: All commands must be run from `.claude/skills/agent-sandboxes/sandbox_cli/` directory.

### Key Command: `sbx browser`

The `browser` command provides visual validation tools for sandbox applications using **Playwright's isolated Chromium**. This does NOT interfere with your Chrome browser - you can use Chrome normally while agents run their own Chromium instances.

```bash
uv run sbx browser <subcommand> [options]

Subcommands:
  start               Start Playwright Chromium with remote debugging
  nav URL            Navigate to a URL
  screenshot         Take a screenshot of the current page
  eval CODE          Execute JavaScript in the page
  pick MESSAGE       Interactive element picker
  cookies            Get all cookies as JSON
  status             Check browser connection status
  close              Close the browser
```

**Browser Workflow**:
```bash
# 1. Start Playwright Chromium in headless mode (no window, background only)
uv run sbx browser start

# 2. Navigate to your sandbox app
uv run sbx browser nav https://5173-sbx_abc123.e2b.app

# 3. Validate visually
uv run sbx browser screenshot --path validation.png

# 4. Check JavaScript state
uv run sbx browser eval "document.title"
uv run sbx browser eval "Array.from(document.querySelectorAll('button')).map(b => b.textContent)"

# 5. Interactive inspection (optional, requires --headed mode)
uv run sbx browser pick "Click the submit button"

# 6. Close when done
uv run sbx browser close
```

**Headless vs Headed Mode**:
```bash
# Headless (default) - runs in background, no window
uv run sbx browser start

# Headed - shows browser window (useful for debugging)
uv run sbx browser start --headed
```

**Prerequisites**:
- Playwright must be installed: `uv pip install playwright`
- Install Playwright's Chromium: `uv run playwright install chromium`
- **NOTE**: Uses Playwright's isolated Chromium (NOT your system Chrome)

**Common Validation Patterns**:

1. **Check page loads**:
   ```bash
   uv run sbx browser nav <public_url>
   uv run sbx browser eval "document.readyState"
   ```

2. **Verify UI elements**:
   ```bash
   uv run sbx browser eval "document.querySelectorAll('button').length"
   uv run sbx browser eval "document.querySelector('h1')?.textContent"
   ```

3. **Check for JavaScript errors**:
   ```bash
   uv run sbx browser eval "window.onerror ? 'Has errors' : 'No errors'"
   ```

4. **Visual regression**:
   ```bash
   uv run sbx browser screenshot --full --path before.png
   # Make changes...
   uv run sbx browser screenshot --full --path after.png
   ```

**Important**:
- Browser commands run on YOUR local machine, not in the sandbox
- Uses **Playwright's isolated Chromium** - does NOT interfere with your Chrome browser
- You can use Chrome normally while agents have their own Chromium instances
- Use these to validate public URLs from sandboxes (after using `get-host`)
- **Runs in headless mode by default** - no browser window appears (background only)
- The browser persists across commands until you `close` it
- **Multiple agents CAN run browsers in parallel** using different ports
- If port 9222 is in use, the CLI will suggest trying a different port (e.g., `--port 9223`)
- All browser commands support the `--port` option for parallel execution

## Multi-Agent Considerations

**CRITICAL**: Multiple agents may be running sandboxes simultaneously. Each agent MUST:

1. **Always use a minimum timeout of `--timeout 1800`** when initializing (30-minute default lifetime) (unless the user specifies a different timeout)
2. **Capture the sandbox ID** from `sbx init` output and remember it in your context
3. **DO NOT use shell variables** like `export SANDBOX_ID=...` (conflicts with other agents)
4. **DO NOT rely on `.sandbox_id` file** (gets overwritten by other agents)
5. **Track the sandbox ID yourself** and use it directly in all subsequent commands
6. **Report the sandbox ID** to the user when done

**Example of proper ID handling**:
```bash
# When you run this:
uv run sbx init

# Capture the sandbox ID from output (e.g., "sbx_abc123def456")
# Store it in YOUR context/memory as: sandbox_id = "sbx_abc123def456"

# Then use it directly in all commands:
uv run sbx exec sbx_abc123def456 "python --version"
uv run sbx files write sbx_abc123def456 /home/user/test.py "print('hello')"
```

## Workflow

### Step 1: Validate Environment

Always start by checking for the E2B_API_KEY:

```bash
cd .claude/skills/agent-sandboxes/sandbox_cli
grep "E2B_API_KEY" ../../../../.env
```

If not found, stop and request the user to add their API key.

### Step 2: Initialize Sandbox and Capture ID

Create a new sandbox with a **30-minute lifetime** and **capture the sandbox ID from the output**:

```bash
cd .claude/skills/agent-sandboxes/sandbox_cli
uv run sbx init --timeout 1800
```

**CRITICAL**:
- **Always use `--timeout 1800`** (30 minutes) - this is the default lifetime for all sandboxes
- The command will output a sandbox ID (e.g., `sbx_abc123def456`)
- **Capture this ID** and remember it in your context
- **DO NOT use environment variables** or files to store it
- **Use this exact ID** in all subsequent commands

Additional options (optional):
- `--template NAME` - Use a specific template (default: base)
- `--env KEY=VALUE` - Set environment variables

Example:
```bash
uv run sbx init --timeout 1800
# Output: Created sandbox: sbx_abc123def456
# YOU remember: sandbox_id = "sbx_abc123def456"
# Sandbox will automatically terminate after 30 minutes
```

### Step 3: Perform Operations

Use the appropriate command based on the task, **using the sandbox ID you captured**:

**Run commands** (replace `<sandbox_id>` with your captured ID):
```bash
uv run sbx exec <sandbox_id> "python --version"
uv run sbx exec <sandbox_id> "pip list" --cwd /home/user/project
```

**File operations**:
```bash
uv run sbx files write <sandbox_id> /home/user/script.py "print('hello')"
uv run sbx files read <sandbox_id> /home/user/output.txt
uv run sbx files upload <sandbox_id> ./local.png /home/user/image.png
```

**IMPORTANT - Writing Files with Special Characters**:
The `sbx files write` command has limitations with special characters like brackets `[]` when passing content as an argument due to shell glob expansion. Use one of these workarounds:

**Option 1: Use --stdin flag (recommended)**:
```bash
# Pipe content through stdin to avoid shell escaping issues
echo 'const arr = [1, 2, 3]; const val = obj["key"];' | uv run sbx files write <sandbox_id> /home/user/file.js --stdin

# Or with heredoc
uv run sbx files write <sandbox_id> /home/user/file.js --stdin << 'EOF'
const arr = [1, 2, 3];
const value = obj["key"];
EOF
```

**Option 2: Write locally, then upload**:
```bash
# Write file locally first (using Write tool)
# Then upload to sandbox - bypasses shell escaping entirely
uv run sbx files upload <sandbox_id> ./local/file.js /home/user/file.js
```

**Option 3: Use sbx exec with heredoc or Python**:
```bash
# Use cat heredoc for complex content
uv run sbx exec <sandbox_id> "cat > /home/user/file.js << 'EOF'
const arr = [1, 2, 3];
const value = obj['key'];
EOF
" --shell

# Or use Python to write files
uv run sbx exec <sandbox_id> "python3 << 'EOF'
with open('/home/user/file.js', 'w') as f:
    f.write('''const arr = [1, 2, 3];
const value = obj[\"key\"];''')
EOF
" --shell
```

**Install packages**:
```bash
# Install uv package manager
uv run sbx exec <sandbox_id> "curl -LsSf https://astral.sh/uv/install.sh | sh" --shell --timeout 120

# Install Python packages
uv run sbx exec <sandbox_id> "/home/user/.local/bin/uv pip install --system requests"
```

### Step 4: Expose Frontend (If Applicable)

**When building applications with a frontend/UI**, create a lightweight server to host your work and expose it:

#### 4.1: Start the Server

**Always default to port 5173** and ensure your frontend is configured to use this port:

```bash
# For Python/Flask
uv run sbx exec <sandbox_id> "python -m http.server 5173" --background --cwd /home/user/project

# For Node/React (Vite)
uv run sbx exec <sandbox_id> "npm run dev -- --port 5173" --background --cwd /home/user/project

# For static HTML/CSS/JS
uv run sbx exec <sandbox_id> "python -m http.server 5173" --background --cwd /home/user/dist

# For a custom Python server
uv run sbx files write <sandbox_id> /home/user/server.py "from flask import Flask; app = Flask(__name__); app.run(host='0.0.0.0', port=5173)"
uv run sbx exec <sandbox_id> "python /home/user/server.py" --background
```

**Key points**:
- Use `--background` flag to keep server running
- **Port 5173 is the default** - use this unless you have a specific reason not to
- Ensure your frontend code is configured for the same port

#### 4.2: Get the Exposed URL

**CRITICAL**: Always use the `get-host` command to retrieve the actual public URL. **Do NOT try to construct or infer the URL**.

```bash
uv run sbx sandbox get-host <sandbox_id> --port 5173
```

This command returns the authoritative public URL (format: `https://5173-<sandbox_id>.e2b.app`).

**Example**:
```bash
uv run sbx sandbox get-host sbx_abc123def456 --port 5173
# Output: https://5173-sbx_abc123def456.e2b.app
# YOU capture and remember this URL in your context
```

**Important**:
- Always use `--port 5173` to match your server port
- Capture the URL in your context/memory (not shell variables)
- Use the exact URL returned by this command
- Do NOT construct URLs manually (they will fail)

#### 4.3: Verify It's Working

Get the URL using `get-host` and test it:
```bash
# Get the URL (captures output: https://5173-<sandbox_id>.e2b.app)
uv run sbx sandbox get-host <sandbox_id> --port 5173

# YOU remember the URL in your context, then test it
curl https://5173-<sandbox_id>.e2b.app
```

**Note**: Capture the URL from get-host output and remember it in your context. Use the exact URL in subsequent commands.

**Important**:
- The server must listen on `0.0.0.0` (not `localhost` or `127.0.0.1`)
- Port must match between server and frontend configuration
- The sandbox will remain alive for 30 minutes (auto-timeout)

### Step 5: Report Results

**Report the results to the user** with the sandbox information:

#### 5.1: Get the Sandbox URL (if frontend/web app)

If you built a frontend or web application, use `get-host` to retrieve the public URL:
```bash
uv run sbx sandbox get-host <sandbox_id> --port 5173
```

This returns the actual URL (e.g., `https://5173-<sandbox_id>.e2b.app`).

**Do NOT construct the URL manually** - always use the `get-host` command.

#### 5.2: Report to User

Provide the user with:
1. **The sandbox ID** - So they can reference it if needed
2. **The URL** (if applicable) - So they can access the application
3. **Timeout information** - Let them know it will auto-terminate in 30 minutes

Example report:
```
✓ Sandbox created successfully!

Sandbox ID: sbx_abc123def456
Application URL: [Use: uv run sbx sandbox get-host sbx_abc123def456 --port 5173]

Your sandbox will automatically terminate in 30 minutes.
```

**Note**: Always get the actual URL using `sbx sandbox get-host <sandbox_id> --port 5173` - never construct it manually.

**IMPORTANT**:
- **Never delete the sandbox unless you're explicitly asked to do so**
- Sandboxes will automatically timeout after 30 minutes

## Examples

**Progressive Disclosure**: Read only the example you need for your specific task.

### Example 1: Run Python Code Safely
**Read when**: User needs to run/test Python code in isolation.
**See**: [examples/01_run_python_code.md](examples/01_run_python_code.md)

Covers: Basic sandbox workflow, writing scripts, executing Python code, capturing sandbox ID.

### Example 2: Test a Package
**Read when**: User needs to install and test Python packages.
**See**: [examples/02_test_package.md](examples/02_test_package.md)

Covers: Installing uv package manager, installing Python packages, testing package functionality.

### Example 3: Clone and Test Repository
**Read when**: User needs to clone a GitHub repo and run tests or commands in it.
**See**: [examples/03_clone_and_test_repo.md](examples/03_clone_and_test_repo.md)

Covers: Git operations, using --cwd flag, running commands in repository context, longer timeouts.

### Example 4: Process Binary Files
**Read when**: User needs to upload, process, or download binary files (images, PDFs).
**See**: [examples/04_process_binary_files.md](examples/04_process_binary_files.md)

Covers: Binary file upload/download, image processing, using appropriate file operations for binary vs text.

### Example 5: Host Frontend Application
**Read when**: User wants to build a web app, UI, dashboard, or any frontend accessible via browser.
**See**: [examples/05_host_frontend.md](examples/05_host_frontend.md)

Covers: Exposing frontends, using port 5173, starting servers in background, getting public URLs, keeping sandboxes alive.

## Important Notes

1. **ALWAYS USE --timeout 1800** - Every sandbox should have a 30-minute lifetime
2. **CAPTURE AND REMEMBER SANDBOX ID** - Store it in your context, don't use shell variables or files
3. **Multi-agent safe** - Each agent tracks its own sandbox ID independently
4. **Always validate E2B_API_KEY first** - Don't proceed without it
5. **Change directory to sandbox_cli** - All commands must be run from there
6. **Use --shell for complex commands** - Enables pipes, redirections, wildcards
7. **Use --cwd instead of cd** - More reliable for working directory changes
8. **Binary files** - Use `upload`/`download` for images, PDFs, executables
9. **Never delete the sandbox unless you're explicitly asked to do so** - Sandboxes auto-timeout after 30 minutes

## Reference

**Built-in CLI Help**:
```bash
cd .claude/skills/agent-sandboxes/sandbox_cli
uv run sbx --help       # Overview of all commands
uv run sbx <command> --help  # Detailed help for specific command
```

For complete command reference and advanced usage, see:
- **CLI Help**: Run `uv run sbx --help` for interactive command reference
- **Full documentation**: `.claude/skills/agent-sandboxes/sandbox_cli/README.md`
- **Architecture details**: Command groups, modules, and design principles
- **Advanced examples**: Multi-step workflows, git operations, package management

## Troubleshooting

**"Need help with a command"**:
- Run `uv run sbx --help` for all available commands
- Run `uv run sbx <command> --help` for specific command details
- All commands have built-in help documentation

**"E2B_API_KEY not found"**:
- Check `.env` file exists in project root
- Verify key is set: `grep E2B_API_KEY .env`
- Add key if missing: `echo "E2B_API_KEY=key" >> .env`

**"Command not found: sbx"**:
- Ensure you're in the sandbox_cli directory
- Run with `uv run sbx` instead of just `sbx`

**"Sandbox timeout"**:
- Increase timeout: `sbx init --timeout 900`
- Use `--timeout` flag on long-running exec commands

**"Permission denied"**:
- Use `--root` flag for system operations
- Check file paths are in `/home/user/` directory

**"Forgot command syntax"**:
- Use `uv run sbx --help` to see command structure
- Each command group has detailed help with examples
