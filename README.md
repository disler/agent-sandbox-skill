# Agent Sandbox Skill

An agent skill for managing isolated execution environments using [E2B Sandboxes](https://e2b.dev/). 
This skill enables AI agents (Gemini CLI, Claude Code, Codex CLI) to safely execute code, build full-stack applications, and perform arbitrary engineering tasks in a secure, isolated sandbox.

Watch the [Gemini 3 Demo](https://youtu.be/V5IhsHEHXOg) or the newer [Claude Opus 4.5](https://youtu.be/3kgx0YxCriM) Demo to understand what this codebase/skill can do for your agentic coding. 

<img src="images/sandboxes.png" alt="Agent Sandboxes" width="800">

## Why Use Agent Sandboxes? The **Value Proposition**
> 
> Agent Sandboxes unlock 3 key capabilities for your agentic engineering:

- **Isolation**: Each agent fork runs in a fully isolated, gated E2B sandbox, this means no matter what your agent does, it's secure and safe from your local filesystem and production environment.
- **Scale**: You can run as many agent forks as you want, each fork is independent and has its own sandbox. This is a very literal way to scale your compute to scale your impact.
- **Agency**: Your agents have full control over the sandbox environment, they can install packages, modify files, run commands, etc. This means they can handle more of the engineering process for you.


## 🚀 Features

*   **Isolated Execution**: Run untrusted code, tests, and binaries safely.
*   **Full-Stack Development**: Scaffold, build, and host Vue + FastAPI + SQLite apps.
*   **Browser Automation**: Built-in Playwright integration for visual validation.
*   **Agent-First Design**: Optimized for CLI agents with structured prompts and robust error handling.
*   **Persistent Context**: Tools to manage sandbox lifecycles across agent turns.

## 🛠️ Setup

### Prerequisites

*   Python >= 3.12
*   `uv` package manager (recommended)
*   E2B Account & API Key

### Installation

1.  **Clone the repository** (if not already done).
2.  **Configure Environment**:
    Create a `.env` file in the project root:
    ```bash
    cp .env.sample .env
    ```
    Add your E2B API key:
    ```env
    E2B_API_KEY=sbx_...
    ```
    *(Get your key from [E2B Dashboard](https://e2b.dev/dashboard/keys))*

3.  **Open your Agentic Coding Tool**:
    Open your Agentic Coding Tool and start prompting!

    ```bash
    claude
    or
    gemini
    or
    codex
    ```

    Then for one of simple tasks run:

    ```bash
    \sandbox <prompt>
    ```

    For complex tasks run
    ```bash
    \plan-build-host-test <prompt> <workflow_id>
    ```

## Starter Prompts

The `prompts/{claude,gemini,codex}/<difficulty>_<task>.md` contain full stack application prompts you can

Try these prompts out with a SOTA Model for the best results.

Run these prompts in your Agentic Coding Tool.

Start with the Very Easy Prompts to get a feel for the tool. Keep in mind token usage increases as the complexity of the prompt increases.

### Very Easy Prompts

```bash
\agent-sandboxes:plan-build-host-test "$(cat prompts/full_stack/codex/very_easy_guestbook.md)" "very_easy_guestbook"
\agent-sandboxes:plan-build-host-test "$(cat prompts/full_stack/codex/very_easy_url_shortener.md)" "very_easy_url_shortener"
\agent-sandboxes:plan-build-host-test "$(cat prompts/full_stack/gemini/very_easy_counter.md)" "very_easy_counter"
\agent-sandboxes:plan-build-host-test "$(cat prompts/full_stack/gemini/very_easy_poll_maker.md)" "very_easy_poll_maker"
\agent-sandboxes:plan-build-host-test "$(cat prompts/full_stack/sonnet/very_easy_calculator.md)" "very_easy_calculator"
\agent-sandboxes:plan-build-host-test "$(cat prompts/full_stack/sonnet/very_easy_counter.md)" "very_easy_counter"
\agent-sandboxes:plan-build-host-test "$(cat prompts/full_stack/sonnet/very_easy_greeter.md)" "very_easy_greeter"
```

### Easy Prompts

```bash
\agent-sandboxes:plan-build-host-test "$(cat prompts/full_stack/gemini/easy_api_mock_studio.md)" "easy_api_mock_studio"
\agent-sandboxes:plan-build-host-test "$(cat prompts/full_stack/gemini/easy_code_snippet_manager.md)" "easy_code_snippet_manager"
\agent-sandboxes:plan-build-host-test "$(cat prompts/full_stack/gemini/easy_cron_heartbeat_monitor.md)" "easy_cron_heartbeat_monitor"
\agent-sandboxes:plan-build-host-test "$(cat prompts/full_stack/gemini/easy_markdown_knowledge_base.md)" "easy_markdown_knowledge_base"
\agent-sandboxes:plan-build-host-test "$(cat prompts/full_stack/gemini/easy_offline_task_board.md)" "easy_offline_task_board"
\agent-sandboxes:plan-build-host-test "$(cat prompts/full_stack/gemini/easy_schema_visualizer.md)" "easy_schema_visualizer"
\agent-sandboxes:plan-build-host-test "$(cat prompts/full_stack/sonnet/easy_nano_banana_simple.md)" "easy_nano_banana_simple"
\agent-sandboxes:plan-build-host-test "$(cat prompts/full_stack/sonnet/easy_notes_app.md)" "easy_notes_app"
\agent-sandboxes:plan-build-host-test "$(cat prompts/full_stack/sonnet/easy_sqlite_crud.md)" "easy_sqlite_crud"
\agent-sandboxes:plan-build-host-test "$(cat prompts/full_stack/sonnet/easy_todo_list.md)" "easy_todo_list"
\agent-sandboxes:plan-build-host-test "$(cat prompts/full_stack/sonnet/easy_chart_sketch.md)" "easy_chart_sketch"
\agent-sandboxes:plan-build-host-test "$(cat prompts/full_stack/sonnet/easy_decision_matrix.md)" "easy_decision_matrix"
\agent-sandboxes:plan-build-host-test "$(cat prompts/full_stack/sonnet/easy_design_system_palette.md)" "easy_design_system_palette"
```

### Medium Prompts

```bash
\agent-sandboxes:plan-build-host-test "$(cat prompts/full_stack/codex/medium_knowledge_base_curator.md)" "medium_knowledge_base_curator"
\agent-sandboxes:plan-build-host-test "$(cat prompts/full_stack/gemini/medium_devops_dashboard.md)" "medium_devops_dashboard"
\agent-sandboxes:plan-build-host-test "$(cat prompts/full_stack/gemini/medium_investment_tracker.md)" "medium_investment_tracker"
\agent-sandboxes:plan-build-host-test "$(cat prompts/full_stack/gemini/medium_log_analysis_tool.md)" "medium_log_analysis_tool"
\agent-sandboxes:plan-build-host-test "$(cat prompts/full_stack/gemini/medium_planning_poker.md)" "medium_planning_poker"
\agent-sandboxes:plan-build-host-test "$(cat prompts/full_stack/opus45/medium_elevenlabs_live_transcription_app.md)" "medium_elevenlabs_live_transcription_app"
\agent-sandboxes:plan-build-host-test "$(cat prompts/full_stack/sonnet/medium_file_explorer.md)" "medium_file_explorer"
\agent-sandboxes:plan-build-host-test "$(cat prompts/full_stack/sonnet/medium_habit_tracker.md)" "medium_habit_tracker"
\agent-sandboxes:plan-build-host-test "$(cat prompts/full_stack/sonnet/medium_nano_banana_generator.md)" "medium_nano_banana_generator"
\agent-sandboxes:plan-build-host-test "$(cat prompts/full_stack/sonnet/medium_personal_finance.md)" "medium_personal_finance"
\agent-sandboxes:plan-build-host-test "$(cat prompts/full_stack/sonnet/medium_recipe_planner.md)" "medium_recipe_planner"
\agent-sandboxes:plan-build-host-test "$(cat prompts/full_stack/sonnet/medium_chart_sketch_pro.md)" "medium_chart_sketch_pro"
```

### Hard Prompts

```bash
\agent-sandboxes:plan-build-host-test "$(cat prompts/full_stack/codex/hard_incident_response_notebook.md)" "hard_incident_response_notebook"
\agent-sandboxes:plan-build-host-test "$(cat prompts/full_stack/codex/hard_learning_cohort_orchestrator.md)" "hard_learning_cohort_orchestrator"
\agent-sandboxes:plan-build-host-test "$(cat prompts/full_stack/codex/hard_supplier_quality_portal.md)" "hard_supplier_quality_portal"
\agent-sandboxes:plan-build-host-test "$(cat prompts/full_stack/codex/hard_ui_design_review_platform.md)" "hard_ui_design_review_platform"
\agent-sandboxes:plan-build-host-test "$(cat prompts/full_stack/sonnet/hard_api_testing.md)" "hard_api_testing"
\agent-sandboxes:plan-build-host-test "$(cat prompts/full_stack/sonnet/hard_code_snippets.md)" "hard_code_snippets"
\agent-sandboxes:plan-build-host-test "$(cat prompts/full_stack/sonnet/hard_content_workflow.md)" "hard_content_workflow"
\agent-sandboxes:plan-build-host-test "$(cat prompts/full_stack/sonnet/hard_freelancer_manager.md)" "hard_freelancer_manager"
\agent-sandboxes:plan-build-host-test "$(cat prompts/full_stack/sonnet/hard_nano_banana_studio.md)" "hard_nano_banana_studio"
\agent-sandboxes:plan-build-host-test "$(cat prompts/full_stack/sonnet/hard_time_tracking.md)" "hard_time_tracking"
```

### Very Hard Prompts

```bash
\agent-sandboxes:plan-build-host-test "$(cat prompts/full_stack/codex/very_hard_analytics_ops_monitoring_hub.md)" "very_hard_analytics_ops_monitoring_hub"
\agent-sandboxes:plan-build-host-test "$(cat prompts/full_stack/codex/very_hard_iot_fleet_maintenance_console.md)" "very_hard_iot_fleet_maintenance_console"
\agent-sandboxes:plan-build-host-test "$(cat prompts/full_stack/codex/very_hard_micro_betting_odds_lab.md)" "very_hard_micro_betting_odds_lab"
\agent-sandboxes:plan-build-host-test "$(cat prompts/full_stack/codex/very_hard_personal_investing_allocator.md)" "very_hard_personal_investing_allocator"
\agent-sandboxes:plan-build-host-test "$(cat prompts/full_stack/codex/very_hard_scriptwriter_automation_workbench.md)" "very_hard_scriptwriter_automation_workbench"
\agent-sandboxes:plan-build-host-test "$(cat prompts/full_stack/sonnet/very_hard_knowledge_base.md)" "very_hard_knowledge_base"
\agent-sandboxes:plan-build-host-test "$(cat prompts/full_stack/sonnet/very_hard_system_monitor.md)" "very_hard_system_monitor"
```

## 3 Browser Testing Prompts

> after you host your app via public url, you can test it with the browser testing prompts.

```bash
# Claude Code only - requires subagent support (parallel=true, headed=true)
/generic-browser-test https://www.anthropic.com/news/claude-opus-4-5 prompts/browser-workflows/opus-4-5-release.md true true

# Sandbox app browser tests (replace <URL> with actual sandbox URL)
/generic-browser-test <URL> prompts/browser-workflows/easy_chart_sketch_browser_test.md true true
/generic-browser-test <URL> prompts/browser-workflows/easy_decision_matrix_browser_test.md true true
/generic-browser-test <URL> prompts/browser-workflows/easy_design_system_palette_browser_test.md true true
/generic-browser-test <URL> prompts/browser-workflows/medium_chart_sketch_pro_browser_test.md true true

# For other agentic coding tools, make sure subagents is false
\generic-browser-test <URL> prompts/browser-workflows/easy_chart_sketch_browser_test.md false true
```

## 🤖 "Reprogrammed" BACKSLASH Commands

This project uses "reprogrammed" backslash commands to trigger agent workflows.
See [CLAUDE.md](CLAUDE.md), [AGENTS.md](AGENTS.md), and [GEMINI.md](GEMINI.md) for more details.

| Command                                                                         | Description                                                                                  |
| :------------------------------------------------------------------------------ | :------------------------------------------------------------------------------------------- |
| `\sandbox <prompt>`                                                             | Small general sandbox operations. An adhoc prompt with minimal compute usage.                |
| `\agent-sandboxes:plan-full-stack <prompt>`                                     | Generates a detailed implementation plan with Browser UI Testing workflows.                  |
| `\agent-sandboxes:build <plan_path>`                                            | Executes a build plan within a sandbox.                                                      |
| `\agent-sandboxes:host <sandbox_id> <port>`                                     | Exposes a port and returns a public URL.                                                     |
| `\agent-sandboxes:test <sandbox_id> <url> <plan_path> <workflow_id>`            | Runs validation tests against the hosted app including browser UI testing.                   |
| `\agent-sandboxes:browser-testing <sandbox_id> <url> <plan_path> <workflow_id>` | Executes browser UI testing workflows from a plan using parallel subagents (headed default). |
| `\agent-sandboxes:plan-build-host-test <prompt> <workflow_id>`                  | **Agentic-Workflow**: Orchestrates a full lifecycle: Plan → Build → Host → Test.             |

## 💻 CLI Usage (Manual)

You can also run the CLI manually for debugging or inspection:

```bash
# From .claude/skills/agent-sandboxes/sandbox_cli/
uv run sbx --help
```

### Common Commands

*   **Init**: `uv run sbx init --timeout 1800`
*   **Execute**: `uv run sbx exec <sandbox_id> "echo hello"`
*   **Files**: `uv run sbx files ls <sandbox_id> /home/user`
*   **Browser**: `uv run sbx browser start`

## 🏗️ Architecture

*   **CLI**: Python-based (`click`, `e2b`, `rich`) located in `.claude/skills/agent-sandboxes/sandbox_cli/`.
*   **Prompts**: Markdown-based prompt templates in `.claude/skills/agent-sandboxes/prompts/`.
*   **Skill Definition**: `SKILL.md` defines the capabilities exposed to the agent.

## 📄 Documentation

*   [Skill Definition & Guide](.claude/skills/agent-sandboxes/SKILL.md)
*   [CLI README](.claude/skills/agent-sandboxes/sandbox_cli/README.md)
*   [E2B Documentation](https://e2b.dev/docs)


## Master **Agentic Coding**
> Prepare for the future of software engineering

Learn tactical agentic coding patterns with [Tactical Agentic Coding](https://agenticengineer.com/tactical-agentic-coding?y=agsbxsk)

Follow the [IndyDevDan YouTube channel](https://www.youtube.com/@indydevdan) to improve your agentic coding advantage.

