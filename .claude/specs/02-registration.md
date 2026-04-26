# Spec: Registration

## Overview
Step 2 wires up the user registration flow for Spendly. The `GET /register` route and its template already exist and render correctly; this step adds the `POST /register` handler that validates the submitted form, inserts a hashed-password user record into the database, and redirects to the login page on success. No session is created at this stage — authentication and session management are handled in Step 3.

## Depends on
Step 1 (Landing page, base layout, database schema). The `users` table is already created by `init_db()` in `database/db.py`, and all auth CSS classes (`.auth-section`, `.auth-card`, `.auth-error`, `.form-input`, `.btn-submit`, etc.) are already defined in `static/css/style.css`.

## Routes
- `POST /register` — validates form data, creates user, redirects to `/login` on success — public

## Database changes
No new tables or columns. Two new helper functions must be added to `database/db.py`:
- `create_user(name, email, password)` — hashes the password, inserts a row into `users`, returns `lastrowid`
- `get_user_by_email(email)` — returns a `sqlite3.Row` or `None`

## Templates
- **Modify:** `templates/register.html` — replace the hardcoded `action="/register"` with `action="{{ url_for('register') }}"`

## Files to change
- `app.py` — set `app.secret_key`; add imports for `request`, `redirect`, `url_for`, `flash`; add the `POST /register` route
- `database/db.py` — add `create_user()` and `get_user_by_email()`
- `templates/register.html` — use `url_for()` in the form action attribute

## Files to create
None beyond this spec.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only (`?` placeholders) — never f-strings in SQL
- Passwords hashed with `werkzeug.security.generate_password_hash` — never store plaintext
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- `app.secret_key` must be set before any `flash()` or session call; a hard-coded dev string is fine for now (e.g. `"dev-secret-change-me"`)
- Duplicate-email errors must be caught via `sqlite3.IntegrityError` in the route (not inside `db.py`) and re-render `register.html` with `error=`
- Validate password length (≥ 8 characters) in the route before touching the DB; re-render with `error=` on failure
- On success, redirect to `url_for('login')` — do **not** auto-login or set a session yet

## Definition of done
- [ ] `GET /register` still renders the form correctly with no console errors
- [ ] Submitting the form with valid name, email, and password (≥ 8 chars) inserts a row into `spendly.db` and redirects to `/login`
- [ ] The stored password in `spendly.db` is a werkzeug hash, not plaintext
- [ ] Submitting with a duplicate email re-renders the form with an inline error (e.g. "Email already registered")
- [ ] Submitting with a password shorter than 8 characters re-renders the form with an inline error (e.g. "Password must be at least 8 characters")
- [ ] Empty fields are blocked by the HTML `required` attribute before the form is submitted
- [ ] The form `action` attribute uses `url_for('register')`, not a hardcoded path
