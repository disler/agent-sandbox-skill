# Learning Cohort Orchestrator

## Objective
Offer a platform to run cohort-based courses with schedules, assignments, live sessions, and learner progress tracking.

## Key Features
- Cohort creation with calendar, modules, and assignment deadlines; time zone aware.
- Live session management (external meeting links) with attendance tracking and reminders.
- Assignments with submissions, rubrics, grading, and feedback; plagiarism check hook (simulated).
- Progress dashboards for learners and instructors; announcements; office hours booking.
- Roles: learner, instructor, TA; permissions by role.

## Data Model Sketch
- Cohorts, Modules, Assignments, Submissions, Grades, Feedback, Sessions, Attendance, Announcements, Users, Roles.

## API/Backend Notes
- Scheduling endpoints; reminder/notification jobs; submission upload with virus scan stub; grading and rubric APIs.
- Attendance logging; plagiarism check stub; role-based access; audit logs for grade changes.
- Calendar export (ICS) and announcement delivery via email/webhook.

## Frontend Notes
- Cohort dashboard, calendar view, assignment submission UI with rubric view, grading workspace for instructors/TAs.
- Attendance markers, office hours scheduler, announcements feed, learner progress visualizations.
- Role-based controls; timezone-aware date displays; accessibility for forms and grading tools.

## Testing & Validation
- Backend: schedule/reminder jobs, submission storage validation, grading/rubric correctness, role checks, attendance logging.
- Frontend: calendar rendering, submission flows, grading interactions, announcements posting, office hours booking.
- Integrated: create cohort, schedule sessions, submit assignments, grade, check progress dashboards; verify reminders fire.

## Success Metrics
- On-time submissions, high reminder delivery rate, accurate grading, and clear progress tracking for cohorts.

