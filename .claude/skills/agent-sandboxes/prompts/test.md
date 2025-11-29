---
model: claude-sonnet-4-5-20250929
description: Validate full-stack application (database, backend, frontend, integration) both internally and externally
argument-hint: [sandbox_id] [public_url] [plan_file_path] [workflow_id]
---

# Purpose

Perform comprehensive testing and validation of a full-stack application running in an E2B sandbox. Tests all three layers (database, backend, frontend) both internally (within sandbox) and externally (via public URL), ensuring the application is production-ready before user access.

## Variables

SANDBOX_ID: $1
PUBLIC_URL: $2
PLAN_FILE_PATH: $3
WORKFLOW_ID: $4
BROWSER_UI_TESTING_SCREENSHOT_PATH: `/temp/<WORKFLOW_ID>/ui-testing/`

## Instructions

- CRITICAL: Both internal AND external validation must pass before reporting success
- CRITICAL: `PLAN_FILE_PATH` is required - re-read the plan to execute Browser UI Testing workflows
- If ANY test fails, debug and fix the issue before continuing
- All three layers (frontend, backend, database) must be validated
- DO NOT proceed to success report if tests fail
- Test real endpoints and user flows, not just health checks
- Verify data persists across the full stack
- Browser UI Testing must execute ALL user story workflows from the plan's `### 7. Browser UI Testing` section

## Workflow

1. **Database Validation (Internal)**
   - Connect to SQLite database in sandbox using `sbx exec [SANDBOX_ID]`
   - Run `sqlite3 [db_path] ".tables"` to verify all tables exist
   - Run `sqlite3 [db_path] "SELECT COUNT(*) FROM [table];"` for main tables
   - Validate schema matches expected structure
   - Store initial row counts for later comparison

2. **Backend Validation (Internal)**
   - Test key API endpoints from inside sandbox:
     - Use `sbx exec [SANDBOX_ID] "curl http://localhost:8000/api/..."` for each endpoint
   - Verify response codes (200, 201, etc.)
   - Verify response data structure is correct
   - Run backend tests if they exist: `sbx exec [SANDBOX_ID] "cd backend && uv run pytest"`
   - Check for errors in backend logs

3. **Backend Validation (External)**
   - Test key API endpoints from OUTSIDE sandbox using PUBLIC_URL:
     - Use `curl [PUBLIC_URL]/api/...` from your local machine
   - Verify responses match internal test results
   - Verify CORS is configured correctly
   - **CRITICAL**: This is the most important test - validates external access works
   - If external tests fail but internal pass:
     - Check CORS configuration in FastAPI
     - Verify backend binds to 0.0.0.0, not 127.0.0.1
     - Check proxy settings in vite.config.js
     - Verify port forwarding and host settings

4. **Frontend Validation (Internal)**
   - Run frontend build: `sbx exec [SANDBOX_ID] "cd frontend && npm run build"`
   - Verify build succeeds with no errors
   - Run frontend tests if they exist: `sbx exec [SANDBOX_ID] "cd frontend && npm test"`
   - Verify dist/ folder is generated

5. **Frontend Validation (External)**
   - Test page loads: `curl [PUBLIC_URL]`
   - Verify HTML is served with correct WORKFLOW_ID in title
   - Verify no 404 errors for static assets
   - Check that frontend can reach backend API

6. **Integration Validation (End-to-End)**
   - Test complete user flow through all layers:
     1. Frontend loads successfully
     2. User performs key action (e.g., create item, submit form)
     3. Frontend makes API call to backend
     4. Backend processes request and updates database
     5. Database stores data correctly
     6. Backend returns data to frontend
     7. Frontend displays updated data
   - Verify data persists after refresh
   - Check browser console for errors (if accessible)
   - Validate the complete flow works from external access

7. **Browser UI Testing (Execute User Story Workflows from Plan)**
   - Run `\agent-sandboxes:browser-testing [SANDBOX_ID] [PUBLIC_URL] [PLAN_FILE_PATH] [WORKFLOW_ID]`
   - This executes all user story workflows from the plan's `### 7. Browser UI Testing` section
   - Each workflow is executed top-to-bottom with error handling and screenshots
   - All workflows must pass before proceeding

8. **Error Resolution (If Tests Fail)**
   - DO NOT proceed if any test fails
   - Debug the specific failure:
     - Check application logs: `sbx exec [SANDBOX_ID] "cat backend/logs/*"`
     - Verify configuration files
     - Test individual components
     - Fix the root cause
   - Re-run ALL validations after fixes
   - Only proceed when all validations pass

9. Now follow the `Report` section to report the validation results

## Report

Present validation results in this format:

## 🧪 Full-Stack Validation Results

**Sandbox ID**: [SANDBOX_ID]
**Public URL**: [PUBLIC_URL]

---

### ✅ Database Validation (Internal)
- **Tables**: ✅ All tables exist ([list table names])
- **Queries**: ✅ Database accessible and queryable
- **Schema**: ✅ Matches expected structure
- **Status**: PASSED

---

### ✅ Backend Validation (Internal)
- **Endpoints Tested**: [list endpoints tested]
- **Response Codes**: ✅ All returned expected codes
- **Data Structure**: ✅ Responses match expected format
- **Tests**: ✅ Backend tests passed (or N/A if no tests)
- **Status**: PASSED

---

### ✅ Backend Validation (External)
- **Endpoints Tested**: [list endpoints tested via PUBLIC_URL]
- **External Access**: ✅ APIs accessible from public URL
- **CORS**: ✅ Configured correctly
- **Data Consistency**: ✅ External responses match internal tests
- **Status**: PASSED

---

### ✅ Frontend Validation (Internal)
- **Build**: ✅ Build succeeded with no errors
- **Tests**: ✅ Frontend tests passed (or N/A if no tests)
- **Assets**: ✅ dist/ folder generated correctly
- **Status**: PASSED

---

### ✅ Frontend Validation (External)
- **Page Load**: ✅ HTML served correctly from [PUBLIC_URL]
- **WORKFLOW_ID**: ✅ Found in page title
- **Static Assets**: ✅ No 404 errors
- **Status**: PASSED

---

### ✅ Integration Validation (End-to-End)
- **User Flow Tested**: [describe the flow, e.g., "Created item → Saved to DB → Displayed in list → Persisted after refresh"]
- **Frontend → Backend**: ✅ API calls successful
- **Backend → Database**: ✅ Data persisted correctly
- **Database → Backend**: ✅ Data retrieved successfully
- **Backend → Frontend**: ✅ Data displayed correctly
- **Data Persistence**: ✅ Data survives page refresh
- **Status**: PASSED

---

### ✅ Browser UI Testing (User Story Workflows from Plan)

**Plan File**: `PLAN_FILE_PATH`

For EACH `### User Story Workflow <N>: <Feature Name>` from the plan's `### 7. Browser UI Testing` section, report:

#### User Story Workflow 1: [Feature Name from Plan]
- **Description**: [one-sentence description from plan]
- **Steps Executed**: [N] of [Total]
- **Screenshot**: [BROWSER_UI_TESTING_SCREENSHOT_PATH]/[workflow-name]-success.png
- **Status**: ✅ PASSED

#### User Story Workflow 2: [Feature Name from Plan]
- **Description**: [one-sentence description from plan]
- **Steps Executed**: [N] of [Total]
- **Screenshot**: [BROWSER_UI_TESTING_SCREENSHOT_PATH]/[workflow-name]-success.png
- **Status**: ✅ PASSED

<repeat for all workflows in the plan>

**OR** (If a workflow failed and could not be resolved):

#### User Story Workflow N: [Feature Name from Plan]
- **Description**: [one-sentence description from plan]
- **Failed At Step**: [step number and description]
- **Error Screenshot**: [BROWSER_UI_TESTING_SCREENSHOT_PATH]/[workflow-name]-error.png
- **Error Details**: [detailed error information]
- **Resolution Attempted**: [what was tried to fix it]
- **Why Unresolved**: [explanation of why the error could not be resolved]
- **Status**: ❌ FAILED

---

### 🎉 Final Validation Status: ALL TESTS PASSED

Your application is production-ready and accessible at: **[PUBLIC_URL]**

**Validation Summary:**
- ✅ Database layer working correctly
- ✅ Backend APIs responding (internal + external)
- ✅ Frontend built and served properly
- ✅ Complete end-to-end flow validated
- ✅ External access confirmed working
- ✅ Browser UI validation passed (screenshot captured)

---

**OR** (If any test failed):

### ❌ Final Validation Status: TESTS FAILED

**Failed Tests:**
- [List which validation section(s) failed]

**Error Details:**
[Detailed error information for each failure]

**Required Actions:**
1. [Specific fix needed for failure 1]
2. [Specific fix needed for failure 2]

**Next Steps:**
- Fix the issues listed above
- Re-run validation: `\agent-sandboxes:test [SANDBOX_ID] [PUBLIC_URL]`
- Do not proceed until all tests pass
