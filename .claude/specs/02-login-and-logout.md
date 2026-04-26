# Spec: Login and Logout

## Overview
This step completes the authentication cycle for Spendly. The `GET /login` route and its template already exist but only render a static form; this step adds the `POST /login` handler that verifies the submitted credentials against the database, creates a Flask session on success, and redirects to the landing page. It also replaces the `/logout` stub with a real implementation that clears the session and redirects to the landing page. The `base.html` navigation is updated to conditionally show a "Sign out" link when a user is logged in, replacing the "Sign in" / "Get started" links.

## Depends on
Step 01 (Landing page, base layout, database schema) and the Registration step — specifically the `users` table and the `get_user_by_email(email)` helper already present in `database/db.py`.

## Routes
- `POST /login` — validates email and password against the `users` table, sets `session['user_id']` on success, redirects to `url_for('landing')` — public
- `GET /logout` — clears the session, redirects to `url_for('landing')` — public (safe to call when not logged in)

## Database changes
No new tables or columns. `get_user_by_email(email)` already exists in `database/db.py` and returns a `sqlite3.Row` or `None`.

## Templates
- **Modify:** `templates/login.html` — change the hardcoded `action="/login"` attribute to `action="{{ url_for('login') }}"`
- **Modify:** `templates/base.html` — update the `.nav-links` block to conditionally render a "Sign out" link (`url_for('logout')`) when `session.get('user_id')` is truthy, and the existing "Sign in" / "Get started" links when it is falsy

## Files to change
- `app.py` — import `session` from `flask`; import `check_password_hash` from `werkzeug.security`; extend the existing `GET /login` route to also accept `POST`; replace the `GET /logout` stub with a real session-clearing implementation
- `templates/login.html` — replace hardcoded `action="/login"` with `action="{{ url_for('login') }}"`
- `templates/base.html` — add conditional nav based on `session.get('user_id')`

## Files to create
None.

## New dependencies
No new dependencies. `werkzeug.security.check_password_hash` is already available from the existing `werkzeug` install.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only (`?` placeholders) — never f-strings in SQL
- Passwords verified with `werkzeug.security.check_password_hash` — never compare plaintext
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- On failed login, re-render `login.html` with `error=` — do **not** redirect (redirecting loses the error without flash)
- Display a single generic error message ("Invalid email or password") for both wrong-email and wrong-password cases — do not reveal which field was wrong
- `session['user_id']` must be stored as an integer (the user's `id` from the DB row)
- Logout must call `session.clear()` — not `session.pop('user_id')` — so any future session keys are also wiped
- Merge the `POST` handler into the existing `login()` function (one route function, `methods=["GET", "POST"]`) — do not create a separate function

## Definition of done
- [ ] `GET /login` renders the sign-in form correctly with no console errors
- [ ] Submitting valid credentials sets `session['user_id']` and redirects to `/`
- [ ] Submitting an unrecognised email re-renders `login.html` with an inline error message
- [ ] Submitting the correct email but wrong password re-renders `login.html` with the same inline error message
- [ ] Empty fields are blocked by the HTML `required` attribute before the form is submitted
- [ ] The form `action` attribute uses `url_for('login')`, not a hardcoded path
- [ ] `GET /logout` clears the session and redirects to `/`
- [ ] Navigating to `/logout` while not logged in redirects cleanly to `/` with no error
- [ ] The navbar shows a "Sign out" link when a session exists and "Sign in" / "Get started" when it does not
