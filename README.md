# SCC CRM Backend

## Setup

```bash
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env              # then edit .env with your real DB password
uvicorn app.main:app --reload --port 8000
```

Visit `http://localhost:8000/docs` for interactive API docs.

## Structure

```
app/
├── main.py           # FastAPI app + CORS + router registration
├── config.py         # loads .env via pydantic-settings
├── database.py       # SQLAlchemy engine, session, get_db dependency
├── models/           # one file per table - matches Simply_Africa.sql exactly
├── schemas/          # Pydantic request/response shapes
└── routers/          # one file per resource - organisations.py is the full template
```

## IMPORTANT: schema mismatch to fix

The uploaded `Simply_Africa.sql` has a bug: the `organisations` table constraint
`uq_org_name_country UNIQUE (name, country)` references a `country` column that
was renamed to `location`. Fix it to:

```sql
CONSTRAINT uq_org_name UNIQUE (name),
```

before running the schema, or the script stops partway through and none of the
tables after `organisations` get created.

## Adding your own table's endpoints

Copy `routers/organisations.py`. Rename the model/schema imports, change the
`prefix` in `APIRouter(...)`, and adjust the fields in your Pydantic schemas.
The five endpoints (list, get one, create, update, delete) follow the same
shape for every table.

Then register your new router in `main.py`:

```python
from app.routers import your_table
app.include_router(your_table.router, prefix="/api")
```

## Dashboard endpoints

`routers/dashboard.py` runs raw SQL against the views in `dashboard_views.sql`
(from the database repo/folder). Run that file against your database before
testing these endpoints, or they'll error with "table doesn't exist".
