# Alembic Database Migration Documentation

---

## 1. Introduction

Alembic is a database migration tool used with SQLAlchemy to manage database schema changes in a safe and structured way. It allows developers to modify database structures over time without deleting existing data, making applications reliable and production-ready.

---

## 2. What is Alembic?

Alembic is a database migration tool that:

- Tracks database schema versions  
- Generates migration scripts automatically  
- Applies incremental schema changes  
- Allows rollback of changes if something goes wrong  

### Without Alembic ❌

```bash
rm database.db
```

- Causes data loss  
- Unsafe approach  
- Not suitable for production  

### With Alembic ✅

```bash
alembic upgrade head
```

- Data is preserved  
- Schema changes are version-controlled  
- Safe for production environments  

---

## 3. Why Alembic is Needed

Database schemas evolve as applications grow. New tables and columns are added, existing fields are modified, and production data must remain intact. Alembic provides a controlled mechanism to handle these changes without risking data loss.

In this project, Alembic is used to manage:

- Users table  
- Todos table  
- Task sharing table  
- Audit logs table  
- Soft delete column (`is_deleted`)  
- Indexes and constraints  

---

## 4. Installing Alembic

Install Alembic using pip:

```bash
pip install alembic
```

---

## 5. Initializing Alembic

Run the following command from the project root directory:

```bash
alembic init alembic
```

This creates the Alembic configuration files, migration environment, and version tracking folder.

---

## 6. Configuring Database Connection

**File:** `alembic.ini`

### For SQLite (development)

```ini
sqlalchemy.url = sqlite:///./auth_todo.db
```

### For PostgreSQL (production)

```ini
sqlalchemy.url = postgresql://user:password@host:port/dbname
```

---

## 7. Linking Alembic to SQLAlchemy Models

Alembic must be connected to the SQLAlchemy models to detect schema changes.

**File:** `alembic/env.py`

```python
from app.database import Base
from app.models.user import User
from app.models.todo import Todo
from app.models.todo_share import TodoShare
from app.models.audit_log import AuditLog

target_metadata = Base.metadata
```

If a model is not imported here, Alembic will not detect its schema changes.

---

## 8. Creating the Initial Migration

Generate the initial migration using:

```bash
alembic revision --autogenerate -m "initial schema"
```

This creates a migration file inside the `alembic/versions/` directory.

---

## 9. Applying Migrations

Apply all migrations to the database:

```bash
alembic upgrade head
```

This command creates tables, applies schema changes, and stores the current version in the `alembic_version` table.

---

## 10. Rolling Back a Migration

If an issue occurs, migrations can be rolled back safely.

Roll back the most recent migration:

```bash
alembic downgrade -1
```

Roll back to a specific version:

```bash
alembic downgrade <revision_id>
```

---

## 11. Conclusion

Alembic provides a reliable and production-safe way to manage database schema changes. By using Alembic, this project avoids manual database deletion, preserves existing data, and maintains a clear version history of schema updates. Its ability to apply and roll back changes ensures stability, scalability, and long-term maintainability of the application.
