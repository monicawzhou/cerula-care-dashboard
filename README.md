# Cerula

Patient management app with a FastAPI backend and React frontend.

---

## Prerequisites

- **Python 3.10+**
- **Node.js 18+** (for the frontend)
- **PostgreSQL** (installed and running)

---

## 1. Python virtual environment

From the project root:

```bash
# Create a virtual environment (pick one name)
python -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate
# On Windows (Command Prompt):
venv\Scripts\activate
# On Windows (PowerShell):
venv\Scripts\Activate.ps1
```

Your prompt should show `(venv)`. Then install backend dependencies:

```bash
cd backend
pip install -r requirements.txt
cd ..
```

---

## 2. PostgreSQL database

Create the database and (if needed) a user.

**Option A – default `postgres` user**

```bash
# Create the database
createdb CerulaAppDatabase
```

**Option B – custom user**

```bash
# In psql or pgAdmin: create a user and database, then:
createdb -U your_username CerulaAppDatabase
```

---

## 3. Database URL

The backend connects to PostgreSQL using a URL in `backend/database.py`:

```python
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:test1234!@localhost:5432/CerulaAppDatabase'
```

Format: `postgresql://USER:PASSWORD@HOST:PORT/DATABASE`

- **USER** – your PostgreSQL username (e.g. `postgres`)
- **PASSWORD** – that user’s password
- **HOST** – usually `localhost`
- **PORT** – usually `5432`
- **DATABASE** – `CerulaAppDatabase` (or the name you used)

Edit `backend/database.py` and set `SQLALCHEMY_DATABASE_URL` to match your user, password, and database.

---

## 4. Run the schema

Create tables and types by running the SQL schema (from project root):

```bash
psql -d CerulaAppDatabase -f backend/sql/schema.sql
```

If you use a specific user:

```bash
psql -U your_username -d CerulaAppDatabase -f backend/sql/schema.sql
```

---

## 5. Seed the database (optional)

Load sample patients, care team members, assignments, and health screenings:

```bash
cd backend
python seed.py
cd ..
```

You’ll be prompted if patients already exist. Run this only when you want to (re)load sample data.

---

## 6. Run the app

**Backend (API)**

```bash
cd backend
# With venv activated (from project root: source venv/bin/activate)
uvicorn main:app --reload
```

API: **http://localhost:8000**  
Docs: **http://localhost:8000/docs**

**Frontend**

In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

App: **http://localhost:5173**

---

## Quick reference

| Step              | Command |
|-------------------|--------|
| Create venv       | `python -m venv venv` |
| Activate venv     | `source venv/bin/activate` (macOS/Linux) or `venv\Scripts\activate` (Windows) |
| Install backend   | `cd backend && pip install -r requirements.txt` |
| Create DB         | `createdb CerulaAppDatabase` |
| Set DB URL        | Edit `backend/database.py` → `SQLALCHEMY_DATABASE_URL` |
| Run schema        | `psql -d CerulaAppDatabase -f backend/sql/schema.sql` |
| Seed DB           | `cd backend && python seed.py` |
| Run backend       | `cd backend && uvicorn main:app --reload` |
| Run frontend      | `cd frontend && npm run dev` |
