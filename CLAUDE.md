# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Activate virtualenv first
source venv/bin/activate

# Run dev server
python manage.py runserver

# Create and apply migrations
python manage.py makemigrations
python manage.py migrate

# System check (no warnings = good)
python manage.py check

# Create superuser for admin
python manage.py createsuperuser

# Lint (check for quote violations and other issues)
ruff check .

# Auto-fix quotes and other fixable issues
ruff check --fix .

# Format code (enforces single quotes)
ruff format .
```

## Architecture

Django 6 + DRF project. Django settings module: `backend.settings`. All apps live under `apps/` and are registered as `apps.<name>` in `INSTALLED_APPS`.

### App dependency order

```
core → academics → staff / students → classes → enrollments
```

- **`apps/core`** — abstract `BaseModel` only. No URLs, no admin. Every model in every other app inherits from it.
- **`apps/academics`** — `Faculty → Department → Program` hierarchy. Foundation for staff, students, and classes.
- **`apps/students`** — `Student` (FK to `Program`).
- **`apps/staff`** — `Teacher` (FK to `Department`).
- **`apps/classes`** — `Subject` (FK to `Program`), `ClassSection` (FK to `Subject` + `Teacher`), `Schedule` (FK to `ClassSection`).
- **`apps/enrollments`** — `Enrollment` (Student × ClassSection, unique together), `Grade` (OneToOne to `Enrollment`).

### BaseModel fields

All models carry: `id` (UUID PK), `created_at`, `updated_at`, `is_deleted`, `deleted_at`. Use `instance.soft_delete()` instead of `.delete()`. All list views filter `is_deleted=False`.

### URL structure

All endpoints are under `/api/v1/`. Each app has its own `urls.py` with path-based routing (no DRF Router — plain `APIView` subclasses). Views follow `<Model>ListView` / `<Model>DetailView` naming with `<uuid:pk>` for detail routes.

### Admin

Site header customized in `backend/urls.py`. Each admin class uses `autocomplete_fields`, `search_fields`, `list_filter`, and computed columns. Inlines: `ScheduleInline` inside `ClassSectionAdmin`, `GradeInline` inside `EnrollmentAdmin`.
