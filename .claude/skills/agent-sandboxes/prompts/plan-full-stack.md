---
description: Creates a full-stack engineering implementation plan with separate frontend, backend, and database layers and saves it to specs directory
argument-hint: [user_prompt]
---

# Quick Plan

Create a detailed implementation plan for a net-new full stack application based on the `USER_PROMPT`. This uses a standardized, pre-validated stack optimized for the E2B sandbox environment. Think deeply and produce a comprehensive specification in `PLAN_OUTPUT_DIRECTORY/<name-of-plan>.md` that another engineer can implement directly. Ensure the plan includes real validation steps—assume the agent has already run the generated application once to confirm it boots before detailing tests.

## Variables

USER_PROMPT: $1
FRONTEND_TOOLING: `vite vue-ts pinia` (static default)
BACKEND_TOOLING: `astral uv python fast api` (static default)
DATABASE_TOOLING: `sqlite` (static default)
PLAN_OUTPUT_DIRECTORY: `<your temp directory>/specs/`
BROWSER_UI_TESTING_STEPS_PER_WORKFLOW: 3-8 (static default)
BROWSER_UI_TESTING_TOTAL_WORKFLOWS: 3-5 (static default)

## Instructions

- IMPORTANT: If no `USER_PROMPT` is provided, stop and ask the user to provide it.
- Carefully analyze the user's requirements provided in the USER_PROMPT variable and expand them into a full-stack scope (frontend + backend + database).
- Determine the task type (chore|feature|refactor|fix|enhancement) and complexity (simple|medium|complex).
- Use the standardized stack: **Vite + Vue 3 + TypeScript + Pinia** frontend, **FastAPI + uvicorn + Python (uv)** backend, and **SQLite** database. These are pre-validated and optimized for the E2B sandbox environment.
- Think deeply (ultrathink) about architecture, request/response flows, data modeling, and environment setup. Keep frontend and backend file layouts clearly separated.
- Explore the codebase (or planned structure) to understand existing patterns and where new frontend, backend, and database artifacts should live.
- Include a nested dependencies section detailing required runtime/build/test tooling per layer (with `uv`/`npm` commands where relevant).
- Define how to test backend services, frontend UI, and database models individually, then together through integrated flows. Assume the agent has already run the application once so we know the scaffold works; testing should include real runs, not hypothetical steps.
- Follow the Plan Format below to create a comprehensive implementation plan, saving it to `PLAN_OUTPUT_DIRECTORY/<descriptive-name>.md`.
- Generate a descriptive, kebab-case filename based on the main topic of the plan.
- Ensure the plan is detailed enough that another developer could follow it to implement the solution, including environment setup, scaffolding commands, and validation steps.
- Consider edge cases, error handling, performance, and scalability concerns.
- BROWSER_UI_TESTING_TOTAL_WORKFLOWS is the total number of user-story workflows to define for browser-based validation.
- BROWSER_UI_TESTING_STEPS_PER_WORKFLOW is the number of UI interaction steps to define for each user-story workflow.
- When writing `### 7. Browser UI Testing` section, be sure to craft the user-stories against the critical paths of the application. Focus on getting the 80/20 of the application working. The core of what was requested by the user.

## Workflow

1. Analyze Requirements - THINK HARD and parse the USER_PROMPT to understand the desired full stack features, user journeys, and constraints.
2. Confirm Stack - Use the standardized stack (Vite + Vue 3 + TypeScript + Pinia, FastAPI + uv, SQLite) and note any prerequisites.
3. Explore/Define Structure - Map out separate frontend and backend directories, database schema files, and shared contracts.
4. Design Solution - Develop architecture, API surface, data models, and UI composition; plan how layers communicate.
5. Document Plan - Write the structured markdown with phases, tasks, dependencies, and testing across backend, frontend, database, and integrated flows.
6. Generate Filename - Create a descriptive kebab-case filename based on the plan's main topic.
7. Browser UI Testing - Define user-story workflows for browser-based validation. Each workflow should have BROWSER_UI_TESTING_STEPS_PER_WORKFLOW steps that validate ONE specific user feature through actual UI interactions.
8. Save & Report - Follow the `Report` section to write the plan to `PLAN_OUTPUT_DIRECTORY/<filename>.md` and provide a summary of key components.

## Plan Format

Follow this format when creating implementation plans:

```md
# Plan: <task name>

## Task Description
<describe the net-new full stack app based on the prompt; call out chosen stacks: frontend = ${FRONTEND_TOOLING}, backend = ${BACKEND_TOOLING}, database = ${DATABASE_TOOLING}>

## Objective
<clearly state what will be accomplished when this plan is complete (running full stack app with separate frontend/backend and DB)>

<if task_type is feature or complexity is medium/complex, include these sections:>
## Problem Statement
<define the specific problem or opportunity this app addresses>

## Solution Approach
<describe the proposed solution approach, end-to-end architecture, and how it addresses the objective; include request/response and data flow>
</if>

## Relevant Files
Use these files and directories to complete the task (frontend and backend must remain separated):

<list existing or to-be-created frontend, backend, and database paths with bullet points explaining why. Include API contracts or shared types where relevant. Include the 'cp .env' (or equivalent) command to copy the .env file into the sandbox if you need to use an API key.>

### New Files
- <new frontend files>
- <new backend files>
- <new database/migration files>
- <shared contracts or env examples>
- <.env file with exact location and api keys we'll need to use in the sandbox>

### Dependencies
- Frontend: <libraries, build tools, test tools; e.g., `npm create vite@latest ... --template vue-ts`, `npm install @testing-library/vue vitest`>
- Backend: <python/uv setup, FastAPI deps, auth/cache libs; e.g., `uv init --app`, `uv add fastapi uvicorn[standard] pydantic`, `uv add --dev pytest httpx`>
- Database: <driver/migration tooling for ${DATABASE_TOOLING}; e.g., `uv add sqlalchemy aiosqlite alembic`>
- Shared/Tooling: <lint/format/test runners, container/scripts; e.g., `npm install --save-dev eslint prettier`, `uv add --dev ruff`, docker-compose if used>

<if complexity is medium/complex, include this section:>
## Implementation Phases
### Phase 1: Foundation
<scaffold frontend and backend projects, initialize database files/migrations, configure environment variables, and run both services once to confirm they boot>

### Phase 2: Core Implementation
<implement backend APIs, database models/migrations/seed data, and frontend views/components that consume the APIs>

### Phase 3: Integration & Polish
<wire frontend to live backend, harden error handling, add observability/logging, polish UI/UX, and prepare deployment assets>
</if>

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

<list step by step tasks as h3 headers with bullet points. Start with scaffolding/bootstrapping, then backend/database, then frontend integration. Last step should validate the work>

### 1. Bootstrap & Verify Stack
- <create frontend and backend folders using the chosen toolchains; initialize gitignore/env files>
- <install dependencies per layer and run both backend and frontend dev servers once to confirm they start; document commands and ports>

### 2. Backend & Database Foundation
- <design DB schema, create migrations/seed data, and set up ORM/validation models>
- <implement base FastAPI app structure, routing, settings, and health endpoints>

### 3. Frontend Foundation
- <configure Vite app with routing/state mgmt, env vars for API base URL, and shared UI shell>
- <add API client/service layer aligned to backend contracts>

### 4. Feature Implementation
- <build backend endpoints for core features with validation, auth, and error handling>
- <build frontend pages/components that call those endpoints and manage state/UI feedback>

### 5. Integration & Observability
- <connect frontend to backend with real data, handle loading/error states, and add logging/metrics as needed>
- <update docs for running services together (scripts, docker-compose, make targets)>

### 6. Testing & Verification
- <backend: unit + integration tests (FastAPI routes, services, database interactions) with realistic data; include coverage of edge cases>
- <database: migration tests, schema validation, and seed verification>
- <frontend: component and integration tests (e.g., Vitest + Testing Library) hitting mocked or test APIs>
- <full-system: end-to-end path that starts backend + frontend together and exercises primary user flows; include a command to run the app and smoke key routes>

<if task_type is feature or complexity is medium/complex, include this section:>
## Testing Strategy
- Backend: <unit tests for services/models, integration tests for FastAPI routes with test DB, contract tests if shared types exist>
- Database: <migration tests, data integrity checks, seed/fixture validation; rollback/forward verification>
- Frontend: <component/unit tests, integration tests hitting stubbed API, visual checks for key screens>
</if>

### 7. Browser UI Testing

Define `BROWSER_UI_TESTING_TOTAL_WORKFLOWS` total user-story workflows for browser-based validation. Each workflow validates ONE specific user feature through `BROWSER_UI_TESTING_STEPS_PER_WORKFLOW` UI interaction steps.

<for each core user feature, create `BROWSER_UI_TESTING_TOTAL_WORKFLOWS` total workflows following this template:>

### User Story Workflow <N>: <Feature Name>
<one-sentence description of what this workflow validates>

- [] Open public URL at `<url>`
- [] <UI action: click, type, select, scroll, etc.>
- [] <UI action>
- [] <UI action - repeat BROWSER_UI_TESTING_STEPS_PER_WORKFLOW times>
- [] CONFIRM: <expected visual/functional outcome>

<example ui validation workflows - replace with actual features from the app:>

### User Story Workflow 1: Create New Item
Validates that a user can successfully create and see a new item in the list.

- [] Open public URL at `https://5173-<sandbox_id>.e2b.app`
- [] Click "Add New" button
- [] Fill in the form fields (name, description)
- [] Click "Save" button
- [] CONFIRM: New item appears in the list with correct data

### User Story Workflow 2: Edit Existing Item
Validates that a user can modify an existing item.

- [] Open public URL and locate an existing item
- [] Click the "Edit" button on the item
- [] Modify one or more fields
- [] Click "Update" button
- [] CONFIRM: Item displays updated values

### User Story Workflow 3: Delete Item
Validates that a user can remove an item.

- [] Open public URL and locate an existing item
- [] Click the "Delete" button
- [] Confirm deletion in the modal/prompt
- [] CONFIRM: Item is removed from the list

<add additional workflows as needed based on the app's core features>

</example ui validation workflows>

## Acceptance Criteria
<list specific, measurable criteria that must be met for the task to be considered complete (running services, passing tests, defined APIs, working UI paths)>

## Validation Commands
Execute these commands to validate the task is complete:

<list precise commands to validate backend, database, frontend, and full-system. Be explicit about starting servers and running tests>
- Example backend: `uv run fastapi dev` and `uv run pytest`
- Example database: `uv run alembic upgrade head` and `uv run pytest tests/db`
- Example frontend: `npm run build && npm run test`
- Example full-stack: `uvicorn src.app:app --port 8000 & npm run dev -- --host 0.0.0.0 --port 5173` then hit health/user flows via curl or e2e tests

## Notes
<additional context, dependencies, or deployment considerations. If new libraries are needed, specify using `uv add` or `npm install`>
```

## Report

After creating and saving the implementation plan, provide a concise report with the following format:

```
✅ Implementation Plan Created

File: PLAN_OUTPUT_DIRECTORY/<filename>.md
Topic: <brief description of what the plan covers>
Key Components:
- <main component 1>
- <main component 2>
- <main component 3>
- <number of user story workflows defined>
```
