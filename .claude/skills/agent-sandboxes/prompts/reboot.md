---
description: Reboot a previously downloaded app by uploading it to a new sandbox and hosting it
argument-hint: [path-to-local-app-directory]
---

# Reboot Application

Upload a local application directory to a new E2B sandbox, read the README to understand setup, setup the application, install dependencies, build the application, and host it. This full-stack application has already been built, we're just re-running it in a new sandbox.

## Variables

APP_LOCAL_DIR: $ARGUMENTS
SANDBOX_TIMEOUT: 43200 (static default)

## Instructions

- If no `APP_LOCAL_DIR` is provided, STOP and ask the user for the path
- Let the README.md guide your setup decisions

## Workflow

1. **Activate Skill** - Activate the agent sandbox skill (`.claude/skills/agent-sandboxes/SKILL.md`)

2. **Create Sandbox** - `uv run sbx init --timeout SANDBOX_TIMEOUT` and capture the sandbox ID

3. **Upload App** - `uv run sbx files upload-dir <sandbox_id> APP_LOCAL_DIR /home/user/app`

4. **Read README** - Find and read the README.md in the uploaded app directory, then follow its instructions for setup

5. **Host App** - Start the app and get public URL via `uv run sbx sandbox get-host <sandbox_id> --port <port>`

6. **Validate** - Curl the public URL from outside the sandbox to confirm it works. If it doesn't work, fix it before stopping.

7. **Test** - Test the application by running your `uv run sbx browser ...` commands to validate the application from the public URL. If anything is not working, fix it before stopping.

## Report

```
✅ Rebooted: APP_LOCAL_DIR
Sandbox ID: <sandbox_id>
Public URL: <url>
```
