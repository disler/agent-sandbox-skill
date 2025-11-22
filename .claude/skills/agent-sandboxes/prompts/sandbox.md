# Purpose

Build and manage E2B sandboxes to run code in isolation.

## Variables

USER_REQUEST: $1

## Workflow

1. Read and execute the `.claude/skills/agent-sandboxes/SKILL.md` file to validate we're ready to run in agent sandboxes.
2. Execute on the `USER_REQUEST` using the sandbox skill to build the request end to end.
3. If the user request you to 'host' the application, be sure to use `get_host` to retrieve the public URL.
   1. Test the application from the outside sandbox with `curl <public url returned from get_host>` to validate the user's access to the application.
   2. Be sure to properly restart the server before presenting the public URL to the user.

## Report

Report execution results to the user. Show the sandbox ID and the URL if applicable.
