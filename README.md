# Backend-UMES

Django REST Framework backend for a University Management System. Covers the full academic structure: faculties, departments, programs, students, teachers, class sections, schedules, enrollments, and grades.

---

## Requirements

- Python 3.12+
- pip

---

## Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd Backend-UMES
```

### 2. Create and activate the virtual environment

**Linux / macOS**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows (Command Prompt)**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**Windows (PowerShell)**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

> If PowerShell blocks the script, run `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned` first.

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Open `.env` and set the values. The only required change for local development is generating a new `SECRET_KEY`. All other defaults work out of the box.

| Variable | Used in | Default |
|---|---|---|
| `SECRET_KEY` | `settings.py` | *(must be set)* |
| `DEBUG` | `settings.py` | `True` |
| `ALLOWED_HOSTS` | `settings.py` | `localhost,127.0.0.1` |
| `DATABASE_URL` | `settings.py` | `sqlite:///db.sqlite3` |
| `LANGUAGE_CODE` | `settings.py` | `en-us` |
| `TIME_ZONE` | `settings.py` | `UTC` |

To switch to PostgreSQL, change `DATABASE_URL`:
```
DATABASE_URL=postgres://user:password@localhost:5432/umes_db
```

### 5. Apply migrations

```bash
python manage.py migrate
```

### 5. Create a superuser (for Admin access)

```bash
python manage.py createsuperuser
```

### 6. Run the development server

```bash
python manage.py runserver
```

The API is available at `http://127.0.0.1:8000/api/v1/`
The Admin panel is available at `http://127.0.0.1:8000/admin/`

---

## API Endpoints

All routes are prefixed with `/api/v1/`.

| Resource | List | Detail |
|---|---|---|
| Faculties | `GET /api/v1/faculties/` | `GET /api/v1/faculties/<uuid>/` |
| Departments | `GET /api/v1/departments/` | `GET /api/v1/departments/<uuid>/` |
| Programs | `GET /api/v1/programs/` | `GET /api/v1/programs/<uuid>/` |
| Students | `GET /api/v1/students/` | `GET /api/v1/students/<uuid>/` |
| Teachers | `GET /api/v1/teachers/` | `GET /api/v1/teachers/<uuid>/` |
| Subjects | `GET /api/v1/subjects/` | `GET /api/v1/subjects/<uuid>/` |
| Class Sections | `GET /api/v1/sections/` | `GET /api/v1/sections/<uuid>/` |
| Schedules | `GET /api/v1/schedules/` | `GET /api/v1/schedules/<uuid>/` |
| Enrollments | `GET /api/v1/enrollments/` | `GET /api/v1/enrollments/<uuid>/` |
| Grades | `GET /api/v1/grades/` | `GET /api/v1/grades/<uuid>/` |

Every list endpoint supports `GET` (list) and `POST` (create).
Every detail endpoint supports `GET`, `PUT`, `PATCH`, and `DELETE` (soft delete).

---

## Project Structure

```
Backend-UMES/
├── manage.py
├── requirements.txt
├── CLAUDE.md
├── backend/                        # Django project configuration
│   ├── settings.py
│   ├── urls.py                     # Root URL conf + admin branding
│   ├── wsgi.py
│   └── asgi.py
└── apps/                           # All application modules
    ├── core/                       # Shared base — no URLs or views
    │   └── models.py               # BaseModel (UUID PK, timestamps, soft delete)
    ├── academics/                  # Academic structure
    │   └── models.py               # Faculty → Department → Program
    ├── students/                   # Student records
    │   └── models.py               # Student (FK to Program)
    ├── staff/                      # Teaching staff
    │   └── models.py               # Teacher (FK to Department)
    ├── classes/                    # Class management
    │   └── models.py               # Subject, ClassSection, Schedule
    └── enrollments/                # Enrollment and grading
        └── models.py               # Enrollment, Grade
```

Each app (except `core`) contains: `models.py`, `serializers.py`, `views.py`, `urls.py`, `admin.py`, `migrations/`.

---

## Data Model Overview

```
Faculty
 └── Department
      ├── Program
      │    ├── Subject
      │    │    └── ClassSection ── Schedule
      │    └── Student
      │         └── Enrollment ── Grade
      └── Teacher ──────────────── ClassSection
```

### Common fields on every model

Every table includes these fields inherited from `BaseModel`:

| Field | Type | Description |
|---|---|---|
| `id` | UUID | Primary key, auto-generated |
| `created_at` | DateTime | Set on creation |
| `updated_at` | DateTime | Updated on every save |
| `is_deleted` | Boolean | Soft delete flag |
| `deleted_at` | DateTime | Timestamp of soft deletion |

`DELETE` requests do not remove records from the database — they set `is_deleted = True`. All list queries exclude soft-deleted records automatically.

---

## Seed Data

The project includes a seed command that populates the database with dummy data for development and testing.

### Quick start

```bash
# Load all seed data
python manage.py seed

# Wipe existing data and re-seed from scratch
python manage.py seed --flush
```

### Options

| Flag | Default | Description |
|---|---|---|
| `--flush` | off | Deletes all existing records before seeding |
| `--students` | `8` | Number of students to create per program |
| `--teachers` | `3` | Number of teachers to create per department |

```bash
# Example: larger dataset
python manage.py seed --flush --students 20 --teachers 5
```

### What gets created (defaults)

| Entity | Count |
|---|---|
| Faculties | 3 |
| Departments | 9 |
| Programs | 11 |
| Teachers | 27 |
| Subjects | 67 |
| Class Sections | 67 |
| Schedules | ~149 |
| Students | 88 |
| Enrollments | ~107 |
| Grades | ~55 |

The command is **idempotent** — running it multiple times without `--flush` will not create duplicate records.

---

## Common Commands

```bash
# Create new migrations after model changes
python manage.py makemigrations

# Apply pending migrations
python manage.py migrate

# Run system checks
python manage.py check

# Open Django shell
python manage.py shell
```
