# Supplier Quality Portal

## Objective
Build a portal for onboarding suppliers, tracking shipments, and managing quality incidents with corrective actions and SLAs.

## Key Features
- Supplier onboarding workflow with document uploads, questionnaires, and approvals; audit trail.
- Shipments tracking with lot numbers, certificates, and status; incident creation tied to shipments/lots.
- Quality incidents with severity, root cause fields, attachments, CAPA actions, and SLA timers.
- Dashboards: supplier scorecards, incident trends, on-time deliveries; export to CSV/PDF.
- Roles: supplier user (limited), internal quality manager, approver.

## Data Model Sketch
- Suppliers, Users, Documents, Shipments, Lots, Incidents, Actions, SLAEvents, Scorecards, Audits.

## API/Backend Notes
- Onboarding workflow endpoints; document upload and verification; incident CRUD with SLA tracking.
- Scorecard calculation job; exports service; role-based access; audit logging.
- Notifications for SLA breaches and approvals; webhooks for ERP integration (simulated).

## Frontend Notes
- Onboarding wizard; shipment list/filter; incident detail with CAPA tasks; dashboard of KPIs.
- Supplier vs internal views; approvals UI; export center; SLA status badges.
- Validation on documents/questionnaires; real-time SLA countdown indicators where useful.

## Testing & Validation
- Backend: onboarding state tests, SLA timers, scorecard math, access control for supplier vs internal, export generation.
- Frontend: form validation, incident workflow interactions, dashboard rendering, role-based view restrictions.
- Integrated: onboard supplier, upload docs, create shipment + incident, run CAPA actions, watch SLA alerts; verify exports work.

## Success Metrics
- SLA adherence, reduced incident reopen rate, accurate scorecards, and zero data leaks across supplier/internal boundaries.

