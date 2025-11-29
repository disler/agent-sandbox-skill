# E2B Sandbox CLI

A streamlined command-line interface for managing E2B sandboxes with a powerful unified command execution interface.

## Installation

```bash
# Install dependencies
uv sync

# Run the CLI
uv run sbx --help
```

## Quick Start

### 1. Initialize a New Sandbox

```bash
# Create a new sandbox with 30-minute timeout
uv run sbx init --timeout 1800

# The command outputs a sandbox ID (e.g., sbx_abc123def)
# IMPORTANT: Capture and remember this ID in your context/memory
# Use it directly in all subsequent commands

# Create with a custom template
uv run sbx init --template claude-code --timeout 1800

# Create with environment variables
uv run sbx init --timeout 1800 --env API_KEY=secret --env DEBUG=true
```

**Critical**: Always use `--timeout 1800` (30 minutes) and remember the sandbox ID in your context.

### 2. File Operations

Replace `<sandbox_id>` with the sandbox ID you captured from init:

```bash
# List files in root directory
uv run sbx files ls <sandbox_id> /

# List files with depth
uv run sbx files ls <sandbox_id> /home/user --depth 2

# Write a file (text)
uv run sbx files write <sandbox_id> /home/user/test.txt "Hello World"

# Read a file (text)
uv run sbx files read <sandbox_id> /home/user/test.txt

# Edit a file (find and replace)
uv run sbx files edit <sandbox_id> /home/user/config.ts --old "old text" --new "new text"

# Edit with replace all
uv run sbx files edit <sandbox_id> /home/user/config.ts --old "find" --new "replace" --all

# Upload a file (binary support - images, PDFs, executables, etc.)
uv run sbx files upload <sandbox_id> /path/to/local/image.png /home/user/image.png

# Download a file (binary support)
uv run sbx files download <sandbox_id> /home/user/output.pdf /path/to/local/output.pdf

# Download entire directory (excludes .venv, node_modules, .git, etc. by default)
uv run sbx files download-dir <sandbox_id> /home/user/project ./local/project

# Download with all files (no exclusions)
uv run sbx files download-dir <sandbox_id> /home/user/project ./local/project --all

# Upload entire directory (excludes .venv, node_modules, .git, etc. by default)
uv run sbx files upload-dir <sandbox_id> ./local/project /home/user/project

# Upload with all files (no exclusions)
uv run sbx files upload-dir <sandbox_id> ./local/project /home/user/project --all

# Check if file exists
uv run sbx files exists <sandbox_id> /home/user/test.txt

# Get file info
uv run sbx files info <sandbox_id> /home/user/test.txt

# Create directory
uv run sbx files mkdir <sandbox_id> /home/user/mydir

# Remove file
uv run sbx files rm <sandbox_id> /home/user/test.txt

# Rename/move file
uv run sbx files mv <sandbox_id> /home/user/old.txt /home/user/new.txt
```

### 3. Command Execution (Unified Interface)

The `exec` command is the most powerful feature - it replaces all specialized commands with a single flexible interface.

Replace `<sandbox_id>` with your captured sandbox ID:

```bash
# Basic execution
uv run sbx exec <sandbox_id> "python --version"

# Run with environment variables
uv run sbx exec <sandbox_id> "echo \$MY_VAR" --env MY_VAR=value

# Run in specific directory
uv run sbx exec <sandbox_id> "pwd" --cwd /home/user/project

# Run as root
uv run sbx exec <sandbox_id> "apt-get update" --root

# Shell features (pipes, redirections, wildcards)
uv run sbx exec <sandbox_id> "ps aux | grep python" --shell

# Background execution
uv run sbx exec <sandbox_id> "sleep 10 && echo done" --background

# Custom timeout
uv run sbx exec <sandbox_id> "long-running-command" --timeout 300

# Combine flags
uv run sbx exec <sandbox_id> "echo \$VAR > output.txt" --shell --env VAR=hello --cwd /home/user
```

### 4. Package Management (via exec)

Instead of specialized commands, use `exec` with package managers:

```bash
# Install uv (Python package manager)
uv run sbx exec <sandbox_id> "curl -LsSf https://astral.sh/uv/install.sh | sh" --shell --timeout 120

# Install Python packages
uv run sbx exec <sandbox_id> "/home/user/.local/bin/uv pip install --system requests pydantic"

# List Python packages
uv run sbx exec <sandbox_id> "/home/user/.local/bin/uv pip list"

# Install bun (JavaScript runtime)
uv run sbx exec <sandbox_id> "curl -fsSL https://bun.sh/install | bash" --shell --timeout 120

# Install Node packages
uv run sbx exec <sandbox_id> "/home/user/.bun/bin/bun add cowsay"

# List Node packages
uv run sbx exec <sandbox_id> "/home/user/.bun/bin/bun pm ls"
```

### 5. Git Operations (via exec)

Use `exec` with the `--cwd` flag for git operations:

```bash
# Clone a repository
uv run sbx exec <sandbox_id> "git clone https://github.com/user/repo /home/user/repo"

# Configure git user
uv run sbx exec <sandbox_id> "git config --global user.email 'user@example.com'" --shell
uv run sbx exec <sandbox_id> "git config --global user.name 'User Name'" --shell

# Check status
uv run sbx exec <sandbox_id> "git status" --cwd /home/user/repo

# Stage files
uv run sbx exec <sandbox_id> "git add ." --cwd /home/user/repo

# Commit changes
uv run sbx exec <sandbox_id> "git commit -m 'Update files'" --cwd /home/user/repo

# View log
uv run sbx exec <sandbox_id> "git log --oneline -n 5" --cwd /home/user/repo

# Pull changes
uv run sbx exec <sandbox_id> "git pull origin main" --cwd /home/user/repo

# Push changes
uv run sbx exec <sandbox_id> "git push origin main" --cwd /home/user/repo
```

### 6. Sandbox Management

```bash
# Create a new sandbox (always use --timeout 1800 for 30 minutes)
uv run sbx sandbox create --template base --timeout 1800

# Create sandbox with custom environment
uv run sbx sandbox create --timeout 1800 --env API_KEY=secret --env DEBUG=true

# Create sandbox with auto-pause (beta)
uv run sbx sandbox create --timeout 1800 --auto-pause

# Connect to existing sandbox
uv run sbx sandbox connect <sandbox_id>

# Get sandbox information
uv run sbx sandbox info <sandbox_id>

# Check if sandbox is running
uv run sbx sandbox status <sandbox_id>

# Pause sandbox (beta)
uv run sbx sandbox pause <sandbox_id>

# Extend sandbox lifetime (adds time to remaining)
uv run sbx sandbox extend-lifetime <sandbox_id> 3600    # Add 1 hour
uv run sbx sandbox extend-lifetime <sandbox_id> 10800   # Add 3 hours
uv run sbx sandbox extend-lifetime <sandbox_id> 43200   # Add 12 hours

# Kill sandbox (only if explicitly requested)
uv run sbx sandbox kill <sandbox_id>
```

**Note**: Sandboxes automatically terminate after the configured timeout. Use `extend-lifetime` to keep them alive longer. Only kill manually if explicitly requested.

### 7. Browser Automation

Browser commands run on your **local machine** using Playwright's isolated Chromium (does not affect your Chrome browser).

```bash
# First-time setup (once per machine)
uv run sbx browser init

# Start browser (headless by default)
uv run sbx browser start
uv run sbx browser start --headed          # Show visible window
uv run sbx browser start --port 9223       # Custom port for parallel agents

# Navigate
uv run sbx browser nav https://example.com

# Execute JavaScript
uv run sbx browser eval "document.title"
uv run sbx browser eval "document.querySelectorAll('button').length"

# Take screenshots
uv run sbx browser screenshot --path screenshot.png
uv run sbx browser screenshot --full       # Full page

# Interact with page
uv run sbx browser click "#submit-button"
uv run sbx browser type "#username" "testuser"
uv run sbx browser scroll down

# Get page structure
uv run sbx browser a11y                    # Accessibility tree (JSON)
uv run sbx browser dom                     # Simplified DOM
uv run sbx browser dom --full              # Raw HTML

# Check status and close
uv run sbx browser status
uv run sbx browser close
```

**Multi-Agent Parallel Execution**: Use `--port` flag with unique ports (9222-9999):
```bash
# Agent 1
uv run sbx browser start --port 9222
uv run sbx browser nav https://app1.example.com --port 9222

# Agent 2 (parallel)
uv run sbx browser start --port 9223
uv run sbx browser nav https://app2.example.com --port 9223
```

**Validating Sandbox Apps**:
```bash
# Get public URL from sandbox
uv run sbx sandbox get-host <sandbox_id> --port 5173

# Validate in browser
uv run sbx browser start
uv run sbx browser nav https://5173-<sandbox_id>.e2b.app
uv run sbx browser eval "document.readyState"
uv run sbx browser screenshot --path validation.png
uv run sbx browser close
```

## Command Structure

The CLI is organized into **five command groups**:

- **`sbx init`** - Quick sandbox initialization with template support
- **`sbx sandbox`** - Sandbox lifecycle management (create, connect, kill, pause, extend-lifetime, info, status)
- **`sbx files`** - File system operations using E2B SDK APIs (ls, read, write, upload, download, rm, mkdir, mv, exists, info)
- **`sbx exec`** - Unified command execution with full control (all flags: --cwd, --user, --root, --shell, --env, --timeout, --background, --stdin)
- **`sbx browser`** - Browser automation for UI validation (init, start, nav, eval, screenshot, click, type, scroll, close)

## Architecture

```
sandbox_cli/
   src/
      main.py              # Main CLI entry point
      commands/            # CLI commands (thin wrappers)
         sandbox.py       # Sandbox lifecycle management
         files.py         # File operations using SDK APIs
         exec.py          # Unified command execution
         browser.py       # Browser automation CLI
      modules/             # Reusable logic modules
          sandbox.py       # Sandbox connection management
          files.py         # File operation helpers
          commands.py      # Command execution helpers
          browser.py       # Browser automation core logic
   pyproject.toml           # Project configuration
   README.md
```

## Key Design Principles

### 1. Unified Command Execution

Instead of having specialized command groups for packages, git, and general commands, we use a single powerful `exec` command that supports:
- Shell features (`--shell` for pipes, redirections, wildcards)
- Working directory (`--cwd`)
- User privileges (`--root` or `--user`)
- Environment variables (`--env`)
- Background execution (`--background`)
- Custom timeouts (`--timeout`)

**Benefits:**
- **80% less code** - Fewer commands to maintain
- **More flexible** - Run ANY command, not just pre-defined ones
- **Agent-friendly** - One interface to learn instead of dozens
- **Composable** - Combine flags for complex operations

### 2. SDK-Based File Operations

File operations use E2B's SDK APIs instead of shell commands for:
- **Reliability** - Structured responses, better error handling
- **Performance** - Direct API calls vs. command execution
- **Type safety** - Returns proper objects with metadata
- **Binary support** - Upload/download any file type (images, PDFs, executables, etc.)

## Features

- **Sandbox Management**: Create, connect, pause, resume, extend lifetime, and kill sandboxes
- **File Operations**: Complete filesystem control with SDK APIs
  - Text file read/write
  - Binary file upload/download (images, PDFs, executables, etc.)
  - Directory operations (list, create, remove, rename)
- **Unified Command Execution**: Run ANY command with full control
- **Environment Variables**: Custom environment configuration
- **Templates**: Support for custom sandbox templates
- **Rich Output**: Beautiful terminal output with tables and colors

## Usage Tips

1. **Remember Sandbox ID**: Always capture and remember the sandbox ID from init output:
   ```bash
   uv run sbx init --timeout 1800
   # Captures output: sbx_abc123def
   # Store in your context/memory, use directly in commands
   ```

2. **Always Use 30-Minute Timeout**: Default timeout for all sandboxes:
   ```bash
   uv run sbx init --timeout 1800  # Always use this
   ```

3. **Use Shell Flag**: For pipes, redirections, and wildcards, use `--shell`:
   ```bash
   uv run sbx exec <sandbox_id> "cat file.txt | grep pattern" --shell
   ```

4. **Working Directory**: Use `--cwd` instead of `cd`:
   ```bash
   uv run sbx exec <sandbox_id> "git status" --cwd /home/user/repo
   ```

5. **Root Privileges**: Use `--root` for system operations:
   ```bash
   uv run sbx exec <sandbox_id> "apt-get install nginx" --root --timeout 300
   ```

6. **Binary Files**: Use upload/download for binary files (images, PDFs, executables):
   ```bash
   # Upload an image
   uv run sbx files upload <sandbox_id> ./local_image.png /home/user/image.png

   # Download generated PDF
   uv run sbx files download <sandbox_id> /home/user/report.pdf ./report.pdf
   ```

## Agent Integration

This CLI is designed to be wrapped and given to AI agents for full sandbox control. The unified `exec` command provides:

- **Predictable interface** - One command signature instead of many
- **Maximum flexibility** - Agents can run ANY shell command
- **Composable operations** - Combine flags for complex scenarios
- **Error handling** - Clear exit codes and error messages

Agents can:
- Create isolated environments
- Install any packages and dependencies
- Run code and commands with full control
- Manage files with structured APIs
- All with a simple, consistent interface

## Examples

### Example 1: Python Development Workflow

```bash
# Initialize sandbox (captures ID: sbx_abc123)
uv run sbx init --timeout 1800

# Install uv package manager
uv run sbx exec <sandbox_id> "curl -LsSf https://astral.sh/uv/install.sh | sh" --shell --timeout 120

# Install Python packages
uv run sbx exec <sandbox_id> "/home/user/.local/bin/uv pip install --system requests beautifulsoup4"

# Create a script using files API
uv run sbx files write <sandbox_id> /home/user/scraper.py "
import requests
from bs4 import BeautifulSoup

response = requests.get('https://example.com')
soup = BeautifulSoup(response.content, 'html.parser')
print(soup.title.string)
"

# Run the script
uv run sbx exec <sandbox_id> "python3 /home/user/scraper.py"

# Sandbox will auto-terminate after 30 minutes
```

### Example 2: Git Workflow

```bash
# Initialize sandbox (captures ID: sbx_def456)
uv run sbx init --timeout 1800

# Configure git
uv run sbx exec <sandbox_id> "git config --global user.email 'dev@example.com' && git config --global user.name 'Developer'" --shell

# Clone repo
uv run sbx exec <sandbox_id> "git clone https://github.com/user/repo /home/user/repo"

# Make changes using files API
uv run sbx files write <sandbox_id> /home/user/repo/README.md "# Updated"

# Commit changes
uv run sbx exec <sandbox_id> "git add . && git commit -m 'Update README'" --shell --cwd /home/user/repo

# View history
uv run sbx exec <sandbox_id> "git log --oneline -n 5" --cwd /home/user/repo

# Sandbox will auto-terminate after 30 minutes
```

### Example 3: Complex Multi-Step Operation

```bash
# Initialize with template (captures ID: sbx_ghi789)
uv run sbx init --template claude-code --timeout 1800 --env PROJECT=myapp

# Create project structure
uv run sbx files mkdir <sandbox_id> /home/user/myapp
uv run sbx files mkdir <sandbox_id> /home/user/myapp/src

# Install dependencies and run tests (combined operation)
uv run sbx exec <sandbox_id> "
  cd /home/user/myapp &&
  python -m venv venv &&
  source venv/bin/activate &&
  pip install pytest &&
  pytest --version
" --shell --timeout 300

# Background task (runs for 30 minutes until auto-timeout)
uv run sbx exec <sandbox_id> "python server.py" --background --cwd /home/user/myapp

# Sandbox will auto-terminate after 30 minutes
```

### Example 4: Working with Binary Files (Images, PDFs, etc.)

```bash
# Initialize sandbox (captures ID: sbx_jkl012)
uv run sbx init --timeout 1800

# Upload an image for processing
uv run sbx files upload <sandbox_id> ./input_photo.jpg /home/user/input.jpg

# Install image processing library
uv run sbx exec <sandbox_id> "curl -LsSf https://astral.sh/uv/install.sh | sh" --shell --timeout 120
uv run sbx exec <sandbox_id> "/home/user/.local/bin/uv pip install --system pillow"

# Process the image (resize, convert format, etc.)
uv run sbx files write <sandbox_id> /home/user/process_image.py "
from PIL import Image

# Open and resize image
img = Image.open('/home/user/input.jpg')
img_resized = img.resize((800, 600))
img_resized.save('/home/user/output.png', 'PNG')
print('Image processed successfully')
"

# Run the processing script
uv run sbx exec <sandbox_id> "python3 /home/user/process_image.py"

# Download the processed image
uv run sbx files download <sandbox_id> /home/user/output.png ./output.png

# Verify the file
ls -lh ./output.png

# Sandbox will auto-terminate after 30 minutes
```

## Comparison: Before vs After

### Before (Specialized Commands):
```bash
# Multiple command groups, each with specific syntax
sbx cmd run <id> "echo hello"
sbx packages install-uv <id>
sbx packages uv <id> --system requests
sbx git clone <id> https://... /path
sbx git status <id> /path
```

### After (Unified Interface):
```bash
# One powerful command with composable flags
sbx exec <id> "echo hello"
sbx exec <id> "curl ... | sh" --shell --timeout 120
sbx exec <id> "uv pip install --system requests"
sbx exec <id> "git clone https://... /path"
sbx exec <id> "git status" --cwd /path
```

**Result:** Fewer concepts to learn, more flexibility, agent-friendly interface.

## Requirements

- Python >= 3.12
- UV package manager
- E2B API key (set in .env file)

## Development

Built with:
- **Click**: Command-line interface framework
- **Rich**: Beautiful terminal output
- **E2B SDK**: Sandbox management
- **UV**: Fast Python package management

## License

Part of the agent-sandboxes project.
