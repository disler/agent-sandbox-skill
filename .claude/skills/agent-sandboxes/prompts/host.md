---
description: Host and expose a web application in E2B sandbox with public URL
argument-hint: [sandbox_id] [port: 5173]
---

# Host Application

Expose and test a web application running in an E2B sandbox by starting the server, retrieving the public URL, and verifying it's accessible.

## Variables

SANDBOX_ID: $1
PORT: $2 default 5173 if not provided

## Instructions

- IMPORTANT: If no `SANDBOX_ID` is provided, stop and ask the user to provide it
- Set up both the client and server applications in the sandbox
- Start the server in background mode on the specified PORT
- Use `sbx sandbox get-host` to retrieve the public URL - NEVER construct it manually
- Validate the application is running with a curl request to the URL
- Report the working URL to the user

## Workflow

1. **Set Up Applications** - Install dependencies and configure both frontend and backend in the sandbox
2. **Start Server** - Launch the web server in background on the specified port
3. **Get Public URL** - Use `sbx sandbox get-host SANDBOX_ID --port PORT` to retrieve the authoritative public URL
4. **Validate** - Test the URL with `curl` OUTSIDE of the sandbox to verify the application is accessible and responding
   - This is a great opportunity to test the application from the outside in, as a user would by using `curl` to verify the application is accessible and responding. Test all endpoints you created in the plan. If something isn't working, fix it before stopping.
   - IMPORTANT: Here you'll might have to configure your host settings, to allow for the **frontend** and **backend** api to be accessible from the outside. This is where iterating and testing is critical.
   - IMPORTANT: Be sure you test against the exposed public URL, not the localhost URL.
   - Many times this means configuring the vite.config.js file to use the exposed public URL.
5. **Report** - Provide the user with the working URL and sandbox information

## Report

Provide the user with the working URL and sandbox information:

```
✅ Application Hosted Successfully

Public URL: <url-from-get-host>
Sandbox ID: SANDBOX_ID
Port: PORT

Your application is now accessible at the URL above.
The sandbox will automatically terminate in 1 hour.
```
