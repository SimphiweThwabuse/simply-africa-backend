from collections import Counter
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.auth.dependencies import get_current_user
from app.database import get_db
from app.models.contact import Contact
from app.models.engagement import Engagement
from app.models.opportunity import Opportunity
from app.models.organisation import Organisation

router = APIRouter(prefix="/reports", tags=["reports"], dependencies=[Depends(get_current_user)])


@router.get("/summary")
def report_summary(db: Session = Depends(get_db)):
    organisations = db.query(Organisation).all()
    opportunities = db.query(Opportunity).all()
    engagements = db.query(Engagement).all()
    return {
        "totals": {
            "organisations": len(organisations),
            "contacts": db.query(Contact).count(),
            "engagements": len(engagements),
            "opportunities": len(opportunities),
        },
        "organisations_by_status": dict(Counter(item.status.value for item in organisations)),
        "opportunities_by_stage": dict(Counter(item.stage.value for item in opportunities)),
        "engagements_by_type": dict(Counter(item.engagement_type.value for item in engagements)),
        "opportunity_value_by_currency": {
            currency: float(sum((item.estimated_value or 0) for item in opportunities if item.currency == currency))
            for currency in {item.currency for item in opportunities}
        },
    }
