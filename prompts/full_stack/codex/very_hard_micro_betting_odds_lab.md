# Micro-Betting Odds Lab

## Objective
Create a controlled micro-betting platform for live games with simulated odds feeds, wallet management (play money), and settlement that enforces exposure and compliance rules.

## Key Features
- Events/games with markets and live odds (pulled from a simulated feed or admin-set).
- Wallets with deposits/withdrawals (play credits) and bet slip with stake/odds/potential return; exposure and limit checks.
- Bet lifecycle: placed -> accepted -> settled; settlement engine via cron/worker; partial voids for canceled markets.
- Admin console: create events/markets, override odds, suspend markets, and view liabilities.
- Risk/compliance: per-user stake limits, velocity checks, geofencing toggle, audit trails.
- Notifications: bet acceptance, settlement results, and exposure alerts.

## Data Model Sketch
- Users, Wallets, Transactions, Events, Markets, Outcomes, OddsTicks, Bets, Settlements, Limits, Audits.

## API/Backend Notes
- Odds feed ingestion (simulated) + WS broadcast; bet placement endpoint with atomic wallet/odds validation; idempotent settlement worker.
- Admin endpoints for market management; risk checks middleware; audit logging.
- Websocket channel for live odds and bet status updates.

## Frontend Notes
- Live event list with markets, odds that auto-refresh via WS, bet slip UI, wallet balance widget, and history.
- Admin panel for odds adjustments and suspension; liability dashboard.
- Error states for suspended markets/limit breaches; optimistic UI gated by server confirmation.

## Testing & Validation
- Backend: bet placement concurrency tests, settlement correctness, limits enforcement, odds feed parsing, WS broadcast tests.
- Frontend: odds update rendering, bet slip flows, admin overrides, suspension handling.
- Integrated: run feed + backend + frontend; place bets during odds changes; settle event; verify wallet balances and audits.

## Success Metrics
- Accurate settlements, zero negative wallet drift, timely odds pushes, and enforced limit/velocity rules.

