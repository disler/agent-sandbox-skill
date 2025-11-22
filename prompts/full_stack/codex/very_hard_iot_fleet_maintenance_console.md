# IoT Fleet Maintenance Console

## Objective
Create a console for managing IoT devices, ingesting telemetry, flagging anomalies, and scheduling maintenance with technician workflows.

## Key Features
- Device registry with ownership, firmware versions, status, and location metadata.
- Telemetry ingestion (batch + streaming simulation), threshold and anomaly detection, health scoring.
- Maintenance tickets with SLA, assignment, checklists, and status transitions; parts inventory linkage.
- Alerts: device offline, high error rate, battery thresholds; suppression windows and escalation.
- Firmware rollout planner with staged cohorts and rollback.

## Data Model Sketch
- Devices, Telemetry, HealthScores, Alerts, Tickets, Technicians, Checklists, Parts, Rollouts, AuditEvents.

## API/Backend Notes
- Ingest endpoints + worker for aggregation; anomaly detection job; health score calculator.
- Ticketing CRUD with SLA timers; alerting engine; firmware rollout orchestration; audit logging.
- Websocket for live device status/alerts updates.

## Frontend Notes
- Device list/map, detail pages with telemetry charts and health badges; ticket board with statuses and technician assignment.
- Alert center with filters/snooze; firmware rollout planner UI; parts association in ticket form.
- Live indicators for online/offline; drill-down to telemetry charts; responsive layouts for field technicians.

## Testing & Validation
- Backend: ingest parsing, anomaly thresholds, health scoring, SLA timers, rollout staging/rollback, audit logging.
- Frontend: telemetry chart rendering, ticket workflows, alert center interactions, rollout planner actions, offline/online badges.
- Integrated: register devices, ingest telemetry, trigger alerts, open/close tickets, stage a rollout, and verify statuses update live.

## Success Metrics
- Accurate health scoring, timely alerts, successful staged rollouts, and on-time ticket resolution rates.

