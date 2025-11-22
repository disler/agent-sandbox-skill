# Personal Investing Allocator

## Objective
Deliver a portfolio cockpit that aggregates broker accounts (mock connectors), tracks holdings and performance, and runs simulated rebalancing and goal-based planning scenarios.

## Key Features
- Account linking (simulated OAuth) with periodic balance/position sync; manual CSV import.
- Portfolio dashboards: holdings by asset class, sector, and region; performance over time; risk score.
- Scenario builder: target allocations, rebalance simulations, tax impact estimation (simplified rules), and recommended trades.
- Alerts: drift thresholds, large drawdowns, and cash buffer reminders.
- Reports: monthly PDF/CSV exports; sharable read-only portfolio views.
- Roles: owner, invited advisor (read-only).

## Data Model Sketch
- Users, Accounts, Positions, Transactions, Prices (cached), Scenarios, Recommendations, Alerts, Reports, Invitations.

## API/Backend Notes
- Data ingestion jobs for positions/transactions; price cache service; drift calculation engine.
- Scenario/rebalance simulation endpoint returning suggested trades; alert scheduler; report generator.
- Permissions enforcing read-only advisor access; audit for exports and simulations.

## Frontend Notes
- Home dashboard with charts, allocation donuts, and trend lines; scenario builder UI with sliders and target mix presets.
- Account linking wizard, CSV import modal, and report export/download center.
- Alerts center with thresholds editing; read-only advisor mode banner and restricted controls.

## Testing & Validation
- Backend: ingest/sync jobs with fixtures, rebalance math correctness, permissions tests, alert scheduling, and PDF generation smoke.
- Frontend: chart rendering, scenario builder interactions, advisor read-only guardrails, alerts editing.
- Integrated: link mock account, import CSV, run scenario, download report, trigger drift alert; verify end-to-end data consistency.

## Success Metrics
- Accurate drift signals, successful report generation, reliable sync cadence, and zero unauthorized writes from advisor role.

