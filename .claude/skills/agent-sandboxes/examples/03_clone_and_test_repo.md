# Example 3: Clone and Test Repository

## When to Use
Read this when you need to clone a GitHub repository and run tests or commands in the repo context.

## User Request Pattern
```
Clone this GitHub repo and run its tests
Test this repository in a sandbox
Clone and build this project
```

## Workflow

### Step 1: Validate Environment
```bash
cd .claude/skills/agent-sandboxes/sandbox_cli
grep "E2B_API_KEY" ../../../../.env
```

### Step 2: Initialize with Longer Timeout
Repositories may take longer to clone and test, so increase the timeout:
```bash
uv run sbx init --timeout 900
# YOU capture and remember: sandbox_id = "sbx_repo123test"
```

### Step 3: Clone Repository
```bash
uv run sbx exec sbx_repo123test "git clone https://github.com/user/repo /home/user/repo"
```

### Step 4: Install Dependencies and Run Tests
Use `--cwd` to run commands in the repository directory:
```bash
uv run sbx exec sbx_repo123test "pip install -r requirements.txt && pytest" --cwd /home/user/repo --shell --timeout 300
```

Key flags:
- `--cwd /home/user/repo` - Run in the repo directory
- `--shell` - Enable shell features for `&&`
- `--timeout 300` - Give tests enough time to complete

### Step 5: Report Results and Clean Up
```bash
uv run sbx sandbox kill sbx_repo123test
```

## Key Points
- Use longer timeout when initializing (--timeout 900 or more)
- Clone to `/home/user/` directory for easy access
- Use `--cwd` flag to run commands in specific directories (better than `cd`)
- Use `--shell` when chaining commands with `&&`
- Increase timeout for long-running tests with `--timeout`
- Git is pre-installed in E2B sandboxes
- Always clean up the sandbox when done
