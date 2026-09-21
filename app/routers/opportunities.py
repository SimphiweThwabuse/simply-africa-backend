from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.auth.dependencies import get_current_user
from app.database import get_db
from app.models.opportunity import Opportunity, OpportunityStage
from app.models.organisation import Organisation
from app.schemas.opportunity import OpportunityCreate, OpportunityList, OpportunityOut, OpportunityUpdate

router = APIRouter(prefix="/opportunities", tags=["opportunities"], dependencies=[Depends(get_current_user)])


def require_organisation(db: Session, organisation_id: int):
    if not db.get(Organisation, organisation_id):
        raise HTTPException(status_code=404, detail="Organisation not found")


def output(opportunity: Opportunity):
    return {
        **{field: getattr(opportunity, field) for field in (
            "id", "organisation_id", "title", "opportunity_type", "stage",
            "estimated_value", "currency", "expected_decision_date", "next_action",
            "owner_id", "created_at",
        )},
        "organisation_name": opportunity.organisation.name,
    }


@router.get("/", response_model=OpportunityList)
def list_opportunities(
    stage: Optional[OpportunityStage] = Query(default=None),
    organisation_id: Optional[int] = Query(default=None),
    db: Session = Depends(get_db),
):
    query = db.query(Opportunity).order_by(Opportunity.created_at.desc())
    if stage is not None:
        query = query.filter(Opportunity.stage == stage)
    if organisation_id is not None:
        query = query.filter(Opportunity.organisation_id == organisation_id)
    items = query.all()
    return {"items": [output(item) for item in items], "total": len(items)}


@router.get("/{opportunity_id}", response_model=OpportunityOut)
def get_opportunity(opportunity_id: int, db: Session = Depends(get_db)):
    opportunity = db.get(Opportunity, opportunity_id)
    if not opportunity:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    return output(opportunity)


@router.post("/", response_model=OpportunityOut, status_code=201)
def create_opportunity(payload: OpportunityCreate, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    require_organisation(db, payload.organisation_id)
    opportunity = Opportunity(**payload.model_dump(), owner_id=current_user.id)
    db.add(opportunity)
    db.commit()
    db.refresh(opportunity)
    return output(opportunity)


@router.put("/{opportunity_id}", response_model=OpportunityOut)
def update_opportunity(opportunity_id: int, payload: OpportunityUpdate, db: Session = Depends(get_db)):
    opportunity = db.get(Opportunity, opportunity_id)
    if not opportunity:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    values = payload.model_dump(exclude_unset=True)
    if "organisation_id" in values:
        require_organisation(db, values["organisation_id"])
    for field, value in values.items():
        setattr(opportunity, field, value)
    db.commit()
    db.refresh(opportunity)
    return output(opportunity)


@router.delete("/{opportunity_id}", status_code=204)
def delete_opportunity(opportunity_id: int, db: Session = Depends(get_db)):
    opportunity = db.get(Opportunity, opportunity_id)
    if not opportunity:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    db.delete(opportunity)
    db.commit()
