from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.auth.dependencies import get_current_user
from app.database import get_db
from app.models.commitment import Commitment, DeliveryStatus
from app.schemas.commitment import CommitmentList

router = APIRouter(prefix="/commitments", tags=["commitments"], dependencies=[Depends(get_current_user)])


def output(commitment: Commitment):
    return {
        "id": commitment.id,
        "organisation_id": commitment.organisation_id,
        "organisation_name": commitment.organisation.name,
        "opportunity_id": commitment.opportunity_id,
        "opportunity_title": commitment.opportunity.title if commitment.opportunity else None,
        "responsible_id": commitment.responsible_id,
        "description": commitment.description,
        "committed_value": commitment.committed_value,
        "due_date": commitment.due_date,
        "delivery_status": commitment.delivery_status,
    }


@router.get("/", response_model=CommitmentList)
def list_commitments(
    delivery_status: Optional[DeliveryStatus] = Query(default=None),
    organisation_id: Optional[int] = Query(default=None),
    db: Session = Depends(get_db),
):
    query = db.query(Commitment).order_by(Commitment.due_date.asc())
    if delivery_status is not None:
        query = query.filter(Commitment.delivery_status == delivery_status)
    if organisation_id is not None:
        query = query.filter(Commitment.organisation_id == organisation_id)
    items = query.all()
    return {"items": [output(item) for item in items], "total": len(items)}
