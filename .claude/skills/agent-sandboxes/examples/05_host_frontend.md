# Example 5: Host Frontend Application

## When to Use
Read this when you're building a web application, UI, or any frontend that needs to be accessible via a browser.

## User Request Pattern
```
Build me a web app/site
Create a dashboard/UI
Make a simple HTML/CSS/JS app
Build a React/Vue/Vite application
I want to see this running in my browser
```

## Workflow

### Step 1: Validate Environment
```bash
cd .claude/skills/agent-sandboxes/sandbox_cli
grep "E2B_API_KEY" ../../../../.env
```

### Step 2: Initialize Sandbox with Longer Timeout
Frontends need time to build and run:
```bash
uv run sbx init --timeout 1800  # 30 minutes
# YOU capture and remember: sandbox_id = "sbx_frontend123app"
```

### Step 3: Build Your Application

#### Option A: Static HTML/CSS/JS
```bash
# Create the HTML file
uv run sbx files write sbx_frontend123app /home/user/app/index.html "
<!DOCTYPE html>
<html>
<head>
    <title>My App</title>
    <style>
        body { font-family: Arial; padding: 20px; }
        .container { max-width: 600px; margin: 0 auto; }
    </style>
</head>
<body>
    <div class='container'>
        <h1>Hello from E2B Sandbox!</h1>
        <p>This app is running on port 5173</p>
    </div>
</body>
</html>
"
```

#### Option B: Python Flask App
```bash
# Install dependencies
uv run sbx exec sbx_frontend123app "curl -LsSf https://astral.sh/uv/install.sh | sh" --shell --timeout 120
uv run sbx exec sbx_frontend123app "/home/user/.local/bin/uv pip install --system flask"

# Create the Flask app
uv run sbx files write sbx_frontend123app /home/user/app.py "
from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def home():
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head><title>Flask App</title></head>
        <body>
            <h1>Flask App on E2B</h1>
            <p>Running on port 5173</p>
        </body>
        </html>
    ''')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5173, debug=True)
"
```

#### Option C: Vite/React App
```bash
# Install Node and create Vite app
uv run sbx exec sbx_frontend123app "curl -fsSL https://bun.sh/install | bash" --shell --timeout 120
uv run sbx exec sbx_frontend123app "/home/user/.bun/bin/bun create vite my-app --template react" --cwd /home/user
uv run sbx exec sbx_frontend123app "/home/user/.bun/bin/bun install" --cwd /home/user/my-app

# Update vite.config.js to use port 5173
uv run sbx files write sbx_frontend123app /home/user/my-app/vite.config.js "
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 5173
  }
})
"
```

### Step 4: Start the Server in Background

**CRITICAL**: Always use port **5173** and run in **background**:

#### For Static Files:
```bash
uv run sbx exec sbx_frontend123app "python -m http.server 5173" --background --cwd /home/user/app
```

#### For Flask:
```bash
uv run sbx exec sbx_frontend123app "python app.py" --background --cwd /home/user
```

#### For Vite/React:
```bash
uv run sbx exec sbx_frontend123app "/home/user/.bun/bin/bun run dev" --background --cwd /home/user/my-app
```

### Step 5: Get the Public URL

**CRITICAL**: Always use the `get-host` command with the port to get the actual URL:

```bash
uv run sbx sandbox get-host sbx_frontend123app --port 5173
```

This returns the authoritative URL:
```
https://5173-sbx_frontend123app.e2b.app
```

**IMPORTANT**:
- **Do NOT construct or infer the URL** - it will fail
- **Always use `sbx sandbox get-host <sandbox_id> --port 5173`**
- Use the exact URL returned by this command

### Step 6: Verify and Share

Get the URL and verify it's working:
```bash
# Get the URL - capture output in your context
uv run sbx sandbox get-host sbx_frontend123app --port 5173
# Output: https://5173-sbx_frontend123app.e2b.app
# YOU remember this URL

# Test it with the URL from above
curl https://5173-sbx_frontend123app.e2b.app
```

Share the URL with the user:
```
Your application is now running at:
https://5173-sbx_frontend123app.e2b.app

The app is hosted on port 5173 and will remain available for 30 minutes (auto-timeout).
```

**Important**: Don't use shell variables for the URL (conflicts with other agents). Capture the get-host output in your context and use it directly.

### Step 7: Report to User

Report the sandbox ID and URL to the user. The sandbox will auto-terminate after 30 minutes.

**Never delete the sandbox unless explicitly asked to do so.**

## Key Points

### Port Configuration
- **Always default to port 5173** unless specified otherwise
- Ensure server listens on `0.0.0.0` (not `localhost` or `127.0.0.1`)
- Configure frontend dev server to use port 5173
- Port must match between server config and frontend config

### Server Requirements
- **Host**: Must be `0.0.0.0` to be accessible externally
- **Port**: Use 5173 by default
- **Background**: Always use `--background` flag to keep server running
- **Timeout**: Increase sandbox timeout for frontends (1800+ seconds)

### Getting the URL
**ONLY METHOD**: Use `sbx sandbox get-host <sandbox_id> --port 5173`

Never construct or infer the URL - always use the get-host command.

### Common Server Commands

**Python Simple HTTP Server** (for static files):
```bash
python -m http.server 5173
```

**Flask**:
```python
app.run(host='0.0.0.0', port=5173)
```

**Vite** (vite.config.js):
```javascript
server: {
  host: '0.0.0.0',
  port: 5173
}
```

**Express** (Node.js):
```javascript
app.listen(5173, '0.0.0.0', () => console.log('Server on 5173'))
```

## Troubleshooting

**"Cannot access the URL"**:
- Verify you used `get-host` command to get the URL (don't construct manually)
- Check server is running: `uv run sbx sandbox status <sandbox_id>`
- Verify port is 5173 in both server and get-host command
- Ensure server listens on `0.0.0.0`, not `localhost`

**"Port already in use"**:
- Kill existing process on port 5173 in sandbox
- Or use a different port (update both server and frontend config)

**"Connection refused"**:
- Server might have crashed - check logs
- Restart server in background
- Verify `--background` flag was used

**"Frontend shows blank page"**:
- Check browser console for errors
- Verify static assets are in correct directory
- Check API endpoints are accessible
- Ensure CORS is configured if needed

## Complete Example: Static Site

```bash
# 1. Initialize
uv run sbx init --timeout 1800
# Captured: sbx_site456

# 2. Create structure
uv run sbx files mkdir sbx_site456 /home/user/site

# 3. Create index.html
uv run sbx files write sbx_site456 /home/user/site/index.html "
<!DOCTYPE html>
<html>
<head>
    <title>My Site</title>
    <style>body{margin:40px auto;max-width:650px;padding:0 10px}</style>
</head>
<body>
    <h1>Welcome!</h1>
    <p>This site is running on E2B at port 5173</p>
</body>
</html>
"

# 4. Start server on port 5173
uv run sbx exec sbx_site456 "python -m http.server 5173" --background --cwd /home/user/site

# 5. Get public URL (capture in your context, not variable)
uv run sbx sandbox get-host sbx_site456 --port 5173
# Returns: https://5173-sbx_site456.e2b.app
# YOU remember: url = "https://5173-sbx_site456.e2b.app"

# 6. Share with user (using the URL you captured)
echo "Visit: https://5173-sbx_site456.e2b.app"

# 7. Sandbox auto-terminates after 30 minutes
# Never kill unless explicitly requested
```
