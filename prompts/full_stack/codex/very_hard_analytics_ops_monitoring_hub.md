# Analytics Ops Monitoring Hub

## Objective
Build a platform to ingest product events, define alert rules, and monitor SLIs/SLOs with dashboards and incident timelines for ops teams.

## Key Features
- Event ingestion API with schema validation and rate limiting; batch ingest endpoint.
- Dimensions/metrics registry; SLI/SLO definitions with burn-rate style alerting; maintenance windows.
- Dashboards: time series charts, breakdowns, error budgets, and annotation overlays.
- Alert rules with channels (email/webhook); incidents with timelines and status (investigating/mitigating/resolved).
- Saved queries and team-based access to dashboards/alerts.

## Data Model Sketch
- Events, Metrics, Dimensions, SLOs, AlertRules, Alerts, Incidents, Dashboards, Queries, Teams, Users.

## API/Backend Notes
- Ingest pipeline with queue + processor; storage tuned for time series (sqlite-friendly rollups ok); query endpoints with filters.
- Alert scheduler evaluating rules and SLO burn rates; webhook/email dispatch.
- RBAC for teams; audit logs for rule changes; maintenance window suppression.

## Frontend Notes
- Dashboard builder with chart presets, SLO cards, and incident overlays; alert rule editor; incident timeline UI.
- Query editor with saved queries; team scoping; notification channel config pages.
- Live auto-refresh for dashboards; status badges for alerts/incidents.

## Testing & Validation
- Backend: ingest validation tests, rollup correctness, alert evaluation against fixtures, RBAC checks, webhook/email mocks.
- Frontend: dashboard rendering, rule editing flows, incident timeline interactions, team scoping guards.
- Integrated: send sample events, create SLO + alert, trigger breach to create incident, resolve incident, verify dashboard updates.

## Success Metrics
- Reliable ingest, timely alert firing, correct burn-rate math, and clear incident timelines without stale statuses.

