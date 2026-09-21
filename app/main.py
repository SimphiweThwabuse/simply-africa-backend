from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import get_db, init_db
from app.routers import organisations, dashboard, auth, contacts, engagements, opportunities, reports, commitments

app = FastAPI(title="Partner & Sponsor CRM API")


@app.on_event("startup")
def startup_event():
    init_db()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# auth has no dependency on get_current_user for /login itself, so it's registered
# like any other router - the protection happens inside each protected route
app.include_router(auth.router, prefix="/api")
app.include_router(organisations.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")
app.include_router(contacts.router, prefix="/api")
app.include_router(engagements.router, prefix="/api")
app.include_router(opportunities.router, prefix="/api")
app.include_router(reports.router, prefix="/api")
app.include_router(commitments.router, prefix="/api")


@app.get("/api/health")
def health():
    """Confirms FastAPI itself is running."""
    return {"status": "ok", "service": "crm-api"}


@app.get("/api/health/db")
def health_db(db: Session = Depends(get_db)):
    """Confirms the backend can actually connect to the configured database."""
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        return {"status": "error", "database": "unreachable", "detail": str(e)}
