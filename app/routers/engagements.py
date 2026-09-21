from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.auth.dependencies import get_current_user
from app.database import get_db
from app.models.contact import Contact
from app.models.engagement import Engagement
from app.models.organisation import Organisation
from app.schemas.engagement import EngagementCreate, EngagementList, EngagementOut, EngagementUpdate

router = APIRouter(prefix="/engagements", tags=["engagements"], dependencies=[Depends(get_current_user)])


def require_organisation(db: Session, organisation_id: int):
    organisation = db.get(Organisation, organisation_id)
    if not organisation:
        raise HTTPException(status_code=404, detail="Organisation not found")
    return organisation


def participants(db: Session, ids: list[int]):
    contacts = db.query(Contact).filter(Contact.id.in_(ids)).all() if ids else []
    if len(contacts) != len(set(ids)):
        raise HTTPException(status_code=404, detail="One or more contacts not found")
    return contacts


def output(engagement: Engagement):
    return {
        "id": engagement.id,
        "organisation_id": engagement.organisation_id,
        "organisation_name": engagement.organisation.name,
        "engagement_type": engagement.engagement_type,
        "occurred_at": engagement.occurred_at,
        "summary": engagement.summary,
        "outcome": engagement.outcome,
        "next_action": engagement.next_action,
        "next_action_date": engagement.next_action_date,
        "participant_ids": [contact.id for contact in engagement.participants],
    }


@router.get("/", response_model=EngagementList)
def list_engagements(
    organisation_id: Optional[int] = Query(default=None),
    from_date: Optional[date] = Query(default=None),
    db: Session = Depends(get_db),
):
    query = db.query(Engagement).order_by(Engagement.occurred_at.desc())
    if organisation_id is not None:
        query = query.filter(Engagement.organisation_id == organisation_id)
    if from_date is not None:
        query = query.filter(Engagement.occurred_at >= from_date)
    items = query.all()
    return {"items": [output(item) for item in items], "total": len(items)}


@router.get("/{engagement_id}", response_model=EngagementOut)
def get_engagement(engagement_id: int, db: Session = Depends(get_db)):
    engagement = db.get(Engagement, engagement_id)
    if not engagement:
        raise HTTPException(status_code=404, detail="Engagement not found")
    return output(engagement)


@router.post("/", response_model=EngagementOut, status_code=201)
def create_engagement(payload: EngagementCreate, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    require_organisation(db, payload.organisation_id)
    engagement = Engagement(**payload.model_dump(exclude={"participant_ids"}), logged_by_id=current_user.id)
    engagement.participants = participants(db, payload.participant_ids)
    db.add(engagement)
    db.commit()
    db.refresh(engagement)
    return output(engagement)


@router.put("/{engagement_id}", response_model=EngagementOut)
def update_engagement(engagement_id: int, payload: EngagementUpdate, db: Session = Depends(get_db)):
    engagement = db.get(Engagement, engagement_id)
    if not engagement:
        raise HTTPException(status_code=404, detail="Engagement not found")
    values = payload.model_dump(exclude_unset=True, exclude={"participant_ids"})
    if "organisation_id" in values:
        require_organisation(db, values["organisation_id"])
    for field, value in values.items():
        setattr(engagement, field, value)
    if payload.participant_ids is not None:
        engagement.participants = participants(db, payload.participant_ids)
    db.commit()
    db.refresh(engagement)
    return output(engagement)


@router.delete("/{engagement_id}", status_code=204)
def delete_engagement(engagement_id: int, db: Session = Depends(get_db)):
    engagement = db.get(Engagement, engagement_id)
    if not engagement:
        raise HTTPException(status_code=404, detail="Engagement not found")
    db.delete(engagement)
    db.commit()
