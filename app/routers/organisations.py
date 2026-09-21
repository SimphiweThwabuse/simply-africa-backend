from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.organisation import Organisation, OrgStatus
from app.models.user import User
from app.auth.dependencies import get_current_user
from app.schemas.organisation import OrganisationCreate, OrganisationUpdate, OrganisationOut

# every route on this router now requires a valid Bearer token
router = APIRouter(prefix="/organisations", tags=["organisations"], dependencies=[Depends(get_current_user)])


@router.get("/", response_model=List[OrganisationOut])
def list_organisations(
    status: Optional[OrgStatus] = None,
    db: Session = Depends(get_db),
):
    """GET /api/organisations  - optionally filter with ?status=active"""
    query = db.query(Organisation)
    if status:
        query = query.filter(Organisation.status == status)
    return query.order_by(Organisation.name).all()


@router.get("/{org_id}", response_model=OrganisationOut)
def get_organisation(org_id: int, db: Session = Depends(get_db)):
    """GET /api/organisations/{id}"""
    org = db.get(Organisation, org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organisation not found")
    return org


@router.post("/", response_model=OrganisationOut, status_code=201)
def create_organisation(payload: OrganisationCreate, db: Session = Depends(get_db)):
    """POST /api/organisations"""
    org = Organisation(**payload.model_dump())
    db.add(org)
    db.commit()
    db.refresh(org)
    return org


@router.put("/{org_id}", response_model=OrganisationOut)
def update_organisation(org_id: int, payload: OrganisationUpdate, db: Session = Depends(get_db)):
    """PUT /api/organisations/{id} - partial update, only sends the fields that changed"""
    org = db.get(Organisation, org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organisation not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(org, field, value)

    db.commit()
    db.refresh(org)
    return org


@router.delete("/{org_id}", status_code=204)
def delete_organisation(org_id: int, db: Session = Depends(get_db)):
    """DELETE /api/organisations/{id}"""
    org = db.get(Organisation, org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organisation not found")
    db.delete(org)
    db.commit()
