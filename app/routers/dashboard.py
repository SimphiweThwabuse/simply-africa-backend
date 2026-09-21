from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/dashboard", tags=["dashboard"], dependencies=[Depends(get_current_user)])

# NOTE: these assume you've run dashboard_views.sql against your database.
# If your teammate's schema doesn't have health_score/v_* views yet, either
# add them (see dashboard_views.sql) or rewrite these as ORM queries instead.


@router.get("/summary")
def summary(db: Session = Depends(get_db)):
    row = db.execute(text("SELECT * FROM v_dashboard_summary")).mappings().one()
    return dict(row)


@router.get("/partner-types")
def partner_types(db: Session = Depends(get_db)):
    rows = db.execute(text("SELECT * FROM v_partner_type_breakdown")).mappings().all()
    return [dict(r) for r in rows]


@router.get("/top-partners")
def top_partners(db: Session = Depends(get_db)):
    rows = db.execute(text("SELECT * FROM v_top_partners_by_health")).mappings().all()
    return [dict(r) for r in rows]


@router.get("/recent-engagements")
def recent_engagements(db: Session = Depends(get_db)):
    rows = db.execute(text("SELECT * FROM v_recent_engagements")).mappings().all()
    return [dict(r) for r in rows]


@router.get("/recent-opportunities")
def recent_opportunities(db: Session = Depends(get_db)):
    rows = db.execute(text("SELECT * FROM v_recent_opportunities")).mappings().all()
    return [dict(r) for r in rows]


@router.get("/upcoming-tasks")
def upcoming_tasks(db: Session = Depends(get_db)):
    rows = db.execute(text("SELECT * FROM v_upcoming_tasks")).mappings().all()
    return [dict(r) for r in rows]
