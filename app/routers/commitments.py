from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database import get_db

from app.models.commitment import Commitment, DeliveryStatus
from app.models.organisation import Organisation
from app.models.opportunity import Opportunity
from app.models.user import User

from app.schemas.commitment import (
    CommitmentCreate,
    CommitmentList,
    CommitmentOut,
    CommitmentUpdate,
)

router = APIRouter(
    prefix="/commitments",
    tags=["commitments"],
    dependencies=[Depends(get_current_user)],
)


def output(commitment: Commitment):
    return {
        "id": commitment.id,
        "organisation_id": commitment.organisation_id,
        "organisation_name": commitment.organisation.name,
        "opportunity_id": commitment.opportunity_id,
        "opportunity_title": (
            commitment.opportunity.title
            if commitment.opportunity
            else None
        ),
        "responsible_id": commitment.responsible_id,
        "responsible_name": (
            commitment.responsible.full_name
            if commitment.responsible
            else None
        ),
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
        query = query.filter(
            Commitment.delivery_status == delivery_status
        )

    if organisation_id is not None:
        query = query.filter(
            Commitment.organisation_id == organisation_id
        )

    items = query.all()

    return {
        "items": [output(item) for item in items],
        "total": len(items),
    }


@router.post(
    "/",
    response_model=CommitmentOut,
    status_code=status.HTTP_201_CREATED,
)
def create_commitment(
    payload: CommitmentCreate,
    db: Session = Depends(get_db),
):
    # Check that the organisation exists
    organisation = db.get(Organisation, payload.organisation_id)

    if not organisation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organisation not found",
        )

    # Check that the opportunity exists, when supplied
    opportunity = None

    if payload.opportunity_id is not None:
        opportunity = db.get(Opportunity, payload.opportunity_id)

        if not opportunity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Opportunity not found",
            )

        # Ensure the opportunity belongs to the selected organisation
        if opportunity.organisation_id != payload.organisation_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Opportunity does not belong to the selected organisation",
            )

    # Check that the responsible user exists and is active
    if payload.responsible_id is not None:
        responsible = db.get(User, payload.responsible_id)

        if not responsible:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Responsible user not found",
            )

        if not responsible.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Responsible user is inactive",
            )

    commitment = Commitment(
        organisation_id=payload.organisation_id,
        opportunity_id=payload.opportunity_id,
        responsible_id=payload.responsible_id,
        description=payload.description,
        committed_value=payload.committed_value,
        due_date=payload.due_date,
        delivery_status=payload.delivery_status,
    )

    db.add(commitment)
    db.commit()
    db.refresh(commitment)

    return output(commitment)


@router.put(
    "/{commitment_id}",
    response_model=CommitmentOut,
)
def update_commitment(
    commitment_id: int,
    payload: CommitmentUpdate,
    db: Session = Depends(get_db),
):
    commitment = db.get(Commitment, commitment_id)

    if not commitment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Commitment not found",
        )

    values = payload.model_dump(exclude_unset=True)

    # Validate organisation if it is being changed
    if "organisation_id" in values:
        if values["organisation_id"] is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Organisation cannot be empty",
            )

        organisation = db.get(
            Organisation,
            values["organisation_id"],
        )

        if not organisation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Organisation not found",
            )

    # Determine the organisation after the update
    final_organisation_id = values.get(
        "organisation_id",
        commitment.organisation_id,
    )

    # Validate opportunity if it is being changed
    if "opportunity_id" in values:
        if values["opportunity_id"] is not None:
            opportunity = db.get(
                Opportunity,
                values["opportunity_id"],
            )

            if not opportunity:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Opportunity not found",
                )

            if opportunity.organisation_id != final_organisation_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Opportunity does not belong to the selected organisation",
                )

    # If organisation changes but opportunity doesn't,
    # make sure the existing opportunity still belongs to it.
    elif "organisation_id" in values and commitment.opportunity_id is not None:
        existing_opportunity = db.get(
            Opportunity,
            commitment.opportunity_id,
        )

        if (
            existing_opportunity
            and existing_opportunity.organisation_id != final_organisation_id
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Existing opportunity does not belong to the selected organisation",
            )

    # Validate responsible user if it is being changed
    if "responsible_id" in values:
        if values["responsible_id"] is not None:
            responsible = db.get(
                User,
                values["responsible_id"],
            )

            if not responsible:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Responsible user not found",
                )

            if not responsible.is_active:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Responsible user is inactive",
                )

    # Description cannot be empty
    if "description" in values:
        if values["description"] is None or not str(values["description"]).strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Description cannot be empty",
            )

    # Delivery status cannot be empty
    if "delivery_status" in values:
        if values["delivery_status"] is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Delivery status cannot be empty",
            )

    # Apply the validated changes
    for field, value in values.items():
        setattr(commitment, field, value)

    db.commit()
    db.refresh(commitment)

    return output(commitment)
@router.delete(
    "/{commitment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_commitment(
    commitment_id: int,
    db: Session = Depends(get_db),
):
    commitment = db.get(Commitment, commitment_id)

    if not commitment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Commitment not found",
        )

    db.delete(commitment)
    db.commit()
    