---
description: Complete full-stack workflow - initialize sandbox, plan, build, and host with public URL
argument-hint: [user_prompt] [workflow_id]
---

# Purpose

This workflow orchestrates a complete full-stack development cycle in an E2B sandbox by initializing a sandbox with an optimized template, creating a full-stack implementation plan, building the application from the plan, and hosting it with a public URL. It uses a standardized, pre-validated stack to ensure fast, reliable builds.

## Variables

USER_PROMPT: $1
WORKFLOW_ID: $2 default "workflow-<hhmmss>+<uuid>" if not provided
FRONTEND_TOOLING: `vite vue-ts pinia` (static default)
BACKEND_TOOLING: `astral uv python fast api` (static default)
DATABASE_TOOLING: `sqlite` (static default)
TEMPLATE_NAME: `fullstack-vue-fastapi-node22` (pre-built E2B template)
PORT: 5173
SANDBOX_CLI_PATH: `temp/<WORKFLOW_ID>/`

## Instructions

- If you ever need to work files locally, always use your `SANDBOX_CLI_PATH` directory. NEVER create files outside of this directory.
- You're free to read out of the local `ai_docs/` and `.env` (if you need an API key) directory if explicitly referenced in the user prompt.
- If you need an API key, cp the `.env` into sandbox (upload it) where you need it (likely the server).
- This is a sequential workflow that must be executed from top to bottom without stopping
- Each step produces outputs that feed into the next step
- All four commands must complete before the workflow is considered done
- If any step fails, report the failure and stop the workflow
- **IMPORTANT**: DO NOT STOP in between steps. Complete every step in the workflow before stopping.
- The sandbox will be initialized first, then the plan created locally, then the build happens in the sandbox, and finally the app is hosted
- Capture the sandbox ID from step 1 to use in subsequent steps
- Capture the plan file path from step 2 to pass to step 3+
- Capture the public URL from step 4 to report to the user
- The host command will determine the appropriate port automatically
- IMPORTANT: You're operating in a sandbox, so unless you have to (download files) DO NOT create files locally. Always use the sandbox. 
- IMPORTANT: You have FULL control over the sandbox, control it fully to get the job done.

## Workflow

> Run the workflow in order, top to bottom. DO NOT STOP in between steps. Complete every step in the workflow before stopping.

0. **Read Agent-Sandboxes Skill Documentation**
   - Read `.claude/skills/agent-sandboxes/SKILL.md` to understand sandbox operations
   - Understand how to use the sandbox CLI, sbx commands, and best practices
   - Take note of all commands available and how to use each.
   - Note the important multi-agent considerations about sandbox ID handling
   - Understand how to expose frontends and retrieve public URLs

1. **Initialize Sandbox**
   - Change to SANDBOX_CLI_PATH directory
   - Run `uv run sbx init --template fullstack-vue-fastapi-node22 --timeout 43200 --name [WORKFLOW_ID]` to create a new sandbox with the optimized template
   - The template includes: Node.js 22, uv, Vite 5.4.11, Vue 3, Pinia, TypeScript (all pre-configured and compatible)
   - This stores the WORKFLOW_ID in the sandbox metadata for tracking
   - Capture the sandbox ID from the output (format: `sbx_abc123def456`)
   - Store the sandbox ID in your working memory for use in subsequent steps
   - Remember: DO NOT use environment variables or files to store the ID

2. **Create Full-Stack Plan**
   - Run `\agent-sandboxes:plan-full-stack [USER_PROMPT]`
   - Uses the standardized stack: Vite + Vue 3 + TypeScript + Pinia, FastAPI + uv, SQLite
   - Generates a comprehensive implementation plan with separated frontend/backend/database layers
   - Captures the path to the generated plan file in specs/ directory
   - Store the path as `path_to_plan` for the next step

3. **Build Application in Sandbox**
   - Run `\build [path_to_plan]`
   - This implements the full-stack application in the E2B sandbox following the plan
   - All work happens in the sandbox using the sandbox ID from step 1
   - Frontend and backend are set up with proper dependencies
   - Make sure the frontend is visually appealing and functional. Avoid color combinations that make the text hard to read.
   - Database schema is initialized
   - All validation commands from the plan are executed
   - Store the build completion status for reporting
   - IMPORTANT: Update the title of the html page your working on to begin with your `WORKFLOW_ID` so we can give you credit for your work.
   - IMPORTANT: As you wrap up this step, be sure to document how to run the frontend, backend, and database in the README.md at the top of your application directory. This will tell future agents and engineers how to run your application. Keep it concise, describe the app, describe requirements, and describe the setup steps to run it, but don't get too verbose. Keep it less than 100 lines.

4. **Host and Expose Application**
   - Run `\host [sandbox_id] [PORT]`
   - This sets up client and server applications in the sandbox
   - Starts the server in background mode on PORT
   - Retrieves the public URL using `sbx sandbox get-host`
   - Validates the application is accessible with curl
   - Store the public URL for the final report
   - Use this as an opportunity to test the application from the outside sandbox.
   - Remember we have to able to access the client and the server from the exposed public URL that you'll build from the get-host command. That means you may have to configure your host settings, to allow for the **frontend** and **backend** api to be accessible from the outside. This is where iterating and testing is critical.
   - IMPORTANT: Be sure you run your final test from OUTSIDE the sandbox to validate the user's access to the application.

5. **Final Testing & Validation**
   - Run `\agent-sandboxes:test [sandbox_id] [public_url] [path_to_plan] [WORKFLOW_ID]`
   - This performs comprehensive validation of database, backend (internal + external), frontend (internal + external), end-to-end integration, and browser UI testing
   - Browser UI Testing executes all user story workflows from the plan's `### 7. Browser UI Testing` section
   - CRITICAL: All tests must pass before proceeding to report
   - If any test fails, the test command will provide specific debugging guidance
   - Re-run the test command after fixes until all validations pass

6. **Report Complete Workflow**
   - Follow the Report section to summarize the complete workflow execution

## Report

Provide a comprehensive workflow summary:

### 🎯 Full-Stack Workflow Complete

**Application Request**: [USER_PROMPT summary]
**Technology Stack**:
- Frontend: Vite + Vue 3 + TypeScript + Pinia
- Backend: FastAPI + uvicorn + Python (uv)
- Database: SQLite
- Template: fullstack-vue-fastapi-node22

---

### Step 1: Sandbox Initialization ✅
**Sandbox ID**: [captured sandbox ID]
**Name**: [WORKFLOW_ID]
**Timeout**: 1 hour
**Status**: Sandbox created and ready

---

### Step 2: Planning ✅ 
**Plan File**: `[path_to_plan]`
**Key Components**:
- [Main component 1 from plan]
- [Main component 2 from plan]
- [Main component 3 from plan]

---

### Step 3: Build ✅
**Sandbox ID**: [SANDBOX_ID]
**Files Modified**: [count from build report]
**Key Changes**:
- [Frontend setup and implementation summary]
- [Backend API and services summary]
- [Database schema and models summary]
- [Validation status: all tests passed]

---

### Step 4: Host ✅
**Public URL**: [url-from-get-host]
**Port**: 5173
**Status**: Application is live and accessible

---

### Step 5: Validation ✅
**Database**: ✅ Tables verified, queries successful
**Backend**: ✅ All endpoints tested (internal + external), CORS configured
**Frontend**: ✅ Build succeeded, page loads, assets served
**Integration**: ✅ End-to-end user flow validated
**Browser UI Testing**: ✅ All user story workflows from plan passed

---

### Final Status

 **Complete workflow finished successfully**

Your full-stack application is now:
- Running in isolated sandbox: **[sandbox_id]**
- Planned with comprehensive specs
- Built and tested
- Hosted and accessible at: **[public URL]**

**Sandbox Details**:
- Sandbox ID: [sandbox_id]
- Auto-terminates in: 1 hour
- Access your app at: [public URL]

**Next Steps**:
- Test the application in your browser
- Review the implementation plan at `[path_to_plan]`
- The sandbox will remain active for 1 hour for testing
