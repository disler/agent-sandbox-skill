# Example 2: Test a Package

## When to Use
Read this when you need to test if a Python package works or install and verify packages in a sandbox.

## User Request Pattern
```
Can you test if the 'requests' package works?
Install and test this package in a sandbox
Check if package X is working correctly
```

## Workflow

### Step 1: Validate Environment
```bash
cd .claude/skills/agent-sandboxes/sandbox_cli
grep "E2B_API_KEY" ../../../../.env
```

### Step 2: Initialize Sandbox and Capture ID
```bash
uv run sbx init
# YOU capture and remember: sandbox_id = "sbx_xyz789abc"
```

### Step 3: Install UV Package Manager
```bash
uv run sbx exec sbx_xyz789abc "curl -LsSf https://astral.sh/uv/install.sh | sh" --shell --timeout 120
```

Note: Use `--shell` flag for piping commands, and increase `--timeout` for installation.

### Step 4: Install the Package
```bash
uv run sbx exec sbx_xyz789abc "/home/user/.local/bin/uv pip install --system requests"
```

### Step 5: Test the Package
```bash
uv run sbx exec sbx_xyz789abc "python3 -c 'import requests; print(requests.__version__)'"
```

### Step 6: Report Results and Clean Up
```bash
uv run sbx sandbox kill sbx_xyz789abc
```

## Key Points
- Install uv package manager first (faster and more reliable than pip)
- Use `--shell` flag when piping commands (curl | sh)
- Set appropriate timeout for installations (120+ seconds)
- Use `/home/user/.local/bin/uv` after installing uv
- Test the package with a simple import or version check
- Always clean up the sandbox when done
