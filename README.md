# Employee Management System (EMS)

A desktop application for managing employee records, built with **Django** (database, ORM, admin) and **Tkinter** (graphical interface).

Django is used as the data layer: the Tkinter GUI talks directly to Django's ORM, so you get models, migrations, and the built-in admin site without needing to run a web server for everyday use.

## Features

- **Add employees** with name, position, department, email, phone, and salary
- **Searchable table** of employees (filters by name, position, email, and department as you type)
- **Soft delete and restore**: employees are never permanently removed; they are marked inactive and can be restored later
- **Show/hide inactive employees** with a single checkbox; inactive rows are greyed out
- **Click a row to select it**: the employee ID is filled in automatically for delete/restore
- **Input validation**: required fields, basic email check, and non-negative salary
- **Live record count** and zebra-striped rows for readability
- **Django admin** with list filters, search, and bulk "soft delete" / "restore" actions

## Tech Stack

- Python 3
- Django 6.1
- Tkinter / ttk (included with most Python installations)
- SQLite (default Django database)

## Project Structure

```
ems_project/
├── manage.py               # Django command-line utility
├── gui_app.py              # Tkinter desktop application
├── db.sqlite3              # SQLite database (created after migrating)
├── ems_project/            # Django project configuration
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
└── employees/              # Django app
    ├── models.py           # Employee model with soft delete / restore
    ├── admin.py            # Customized admin with bulk actions
    ├── views.py
    ├── tests.py
    └── migrations/
```

## Data Model

**Employee**

| Field          | Type             | Notes                                                                 |
|----------------|------------------|-----------------------------------------------------------------------|
| `id`           | BigAutoField     | Primary key, auto-generated                                           |
| `name`         | CharField        | Max 100 characters                                                    |
| `position`     | CharField        | Max 100 characters                                                    |
| `email`        | EmailField       | Optional                                                              |
| `phone`        | CharField        | Optional, max 30 characters                                           |
| `department`   | CharField        | One of: Engineering, HR, Finance, Marketing, Sales, Operations, IT Support (default: Operations) |
| `salary`       | DecimalField     | Up to 10 digits, 2 decimal places (default: 0)                        |
| `is_available` | BooleanField     | `True` = active, `False` = soft-deleted (default: `True`)             |
| `date_hired`   | DateTimeField    | Set automatically on creation                                         |

Model methods:

- `soft_delete()` sets `is_available` to `False`
- `restore()` sets `is_available` back to `True`

Records are ordered by `id`.

## Getting Started

### 1. Clone the repository and enter the project folder

```bash
git clone <your-repo-url>
cd ems_project
```

### 2. (Optional) Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate      # macOS / Linux
venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install django
```

### 4. Apply database migrations

```bash
python manage.py makemigrations employees
python manage.py migrate
```

> `makemigrations` is only needed if the migration files for the newer fields (email, phone, department, salary, is_available) are not already in `employees/migrations/`.

### 5. Run the desktop app

```bash
python gui_app.py
```

## Using the App

1. **Add an employee**: fill in the form on the left and click **Add Employee**. Name and position are required.
2. **Search**: type in the search box above the table to filter results instantly.
3. **Soft delete**: select a row (or type an ID) in the *Delete / Restore by ID* panel and click **Delete (soft)**. You'll be asked to confirm.
4. **Restore**: tick **Show inactive**, select the inactive employee, and click **Restore**.

## Using the Django Admin (Optional)

```bash
python manage.py createsuperuser
python manage.py runserver
```

Open <http://127.0.0.1:8000/admin/> and log in. From the Employee list you can filter by availability and department, search by name, position, or email, and use the bulk actions to soft delete or restore selected employees.

## How It Works

`gui_app.py` sets the `DJANGO_SETTINGS_MODULE` environment variable and calls `django.setup()` before importing the `Employee` model. After that, the GUI uses the ORM exactly as a Django view would (`Employee.objects.create()`, `.filter()`, `Q` lookups for search), and the same database is shared with the admin site.

## Notes

- `DEBUG = True` and the included `SECRET_KEY` are for development only. Change both before any production deployment.
- Tkinter must be available in your Python installation. On some Linux distributions, install it separately (e.g., `sudo apt install python3-tk`).
- The GUI's fonts (Segoe UI) fall back to a system default on non-Windows platforms.

## Roadmap

- Edit existing employee records
- Export to CSV
- Sorting by column
- Unit tests for the model and soft-delete logic
