# Civic Reporter -- setup + login (step 1)

This is the first slice of the project: just App1_accounts (User +
AuthorityProfile) and a minimal App2_reports stub (Area + Category,
needed only because User.area points at it). Report, ReportStatusHistory,
Verification, Comment, Upvote and Notification come in the next step.

## Run it

    python -m venv venv
    source venv/bin/activate        # venv\Scripts\activate on Windows
    pip install -r requirements.txt
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver

## Endpoints

| Method | URL                        | Auth required | Purpose                          |
|--------|----------------------------|----------------|-----------------------------------|
| POST   | /api/auth/register/        | no             | citizen sign-up, returns tokens   |
| POST   | /api/auth/login/            | no             | {"email", "password"} -> tokens  |
| POST   | /api/auth/token/refresh/    | no             | {"refresh"} -> new access token  |
| GET    | /api/auth/me/                | yes (Bearer)   | current user, incl. is_authority |
| GET/POST | /api/reports/areas/       | yes            | list/create Area                  |
| GET/POST | /api/reports/categories/  | yes            | list/create Category              |

Authenticated requests: `Authorization: Bearer <access_token>`.

## Key design points (match the class diagram)

- **No `role` field.** Whether a user is an authority is decided purely by
  whether an `AuthorityProfile` row exists for them: `user.is_authority`
  (a property on `User`) checks this with `hasattr(self, "authorityprofile")`.
  Citizen and authority share the exact same `User` table/login -- an
  authority account is just a `User` row that also has a matching
  `AuthorityProfile` row.
- **Login is email-based**, not username-based (`USERNAME_FIELD = "email"`).
- Authority accounts aren't self-registered through `/register/` on purpose --
  create them via Django admin (`/admin/`) by adding an `AuthorityProfile`
  for an existing user, or build a dedicated internal endpoint later.

Tested end-to-end (register -> login -> authenticated /me/ ->
is_authority flips True after adding an AuthorityProfile) before
this was handed to you.
