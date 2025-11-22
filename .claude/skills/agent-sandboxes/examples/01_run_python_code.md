# Example 1: Run Python Code Safely

## When to Use
Read this when you need to run Python code in a sandbox for testing or execution.

## User Request Pattern
```
Run this Python script in a sandbox to test it
Test this Python code safely
Execute this script in isolation
```

## Workflow

### Step 1: Validate E2B_API_KEY
```bash
cd .claude/skills/agent-sandboxes/sandbox_cli
grep "E2B_API_KEY" ../../../../.env
```

### Step 2: Navigate to CLI Directory
```bash
cd .claude/skills/agent-sandboxes/sandbox_cli
```

### Step 3: Initialize Sandbox and Capture ID
```bash
uv run sbx init
# Output: Created sandbox: sbx_abc123def456
# YOU remember: sandbox_id = "sbx_abc123def456"
```

### Step 4: Write the Script
Using the captured sandbox ID:
```bash
uv run sbx files write sbx_abc123def456 /home/user/test.py "import sys; print(sys.version)"
```

### Step 5: Run the Script
```bash
uv run sbx exec sbx_abc123def456 "python3 /home/user/test.py"
```

### Step 6: Clean Up
```bash
uv run sbx sandbox kill sbx_abc123def456
```

## Key Points
- Always capture and remember the sandbox ID from init output
- Use the captured ID directly in all subsequent commands
- Write files using `sbx files write` command
- Execute with `sbx exec` command
- Always clean up by killing the sandbox when done
