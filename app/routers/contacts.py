from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.auth.dependencies import get_current_user
from app.database import get_db
from app.models.contact import Contact
from app.models.organisation import Organisation
from app.schemas.contact import ContactCreate, ContactOut, ContactUpdate

router = APIRouter(prefix="/contacts", tags=["contacts"], dependencies=[Depends(get_current_user)])


def require_organisation(db: Session, organisation_id: int):
    if not db.get(Organisation, organisation_id):
        raise HTTPException(status_code=404, detail="Organisation not found")


@router.get("/", response_model=list[ContactOut])
def list_contacts(organisation_id: Optional[int] = Query(default=None), db: Session = Depends(get_db)):
    query = db.query(Contact).order_by(Contact.full_name)
    if organisation_id is not None:
        query = query.filter(Contact.organisation_id == organisation_id)
    return query.all()


@router.get("/{contact_id}", response_model=ContactOut)
def get_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.get(Contact, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@router.post("/", response_model=ContactOut, status_code=201)
def create_contact(payload: ContactCreate, db: Session = Depends(get_db)):
    require_organisation(db, payload.organisation_id)
    contact = Contact(**payload.model_dump())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


@router.put("/{contact_id}", response_model=ContactOut)
def update_contact(contact_id: int, payload: ContactUpdate, db: Session = Depends(get_db)):
    contact = db.get(Contact, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    values = payload.model_dump(exclude_unset=True)
    if "organisation_id" in values:
        require_organisation(db, values["organisation_id"])
    for field, value in values.items():
        setattr(contact, field, value)
    db.commit()
    db.refresh(contact)
    return contact


@router.delete("/{contact_id}", status_code=204)
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.get(Contact, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    db.delete(contact)
    db.commit()
