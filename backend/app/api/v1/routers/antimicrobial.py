from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.antimicrobial import AntimicrobialCreate, AntimicrobialUpdate, AntimicrobialOut
from app.services import antimicrobial_service
from app.auth.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/antimicrobials", tags=["Antimicrobials"])


@router.post("/", response_model=AntimicrobialOut, status_code=status.HTTP_201_CREATED)
def create_antimicrobial(
    data: AntimicrobialCreate,
    db: Session = Depends(get_db),
    user:User=Depends(get_current_user),
):
    if antimicrobial_service.get_by_name(db, data.name):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Antimicrobial with this name already exists")
    return antimicrobial_service.create_antimicrobial(db, data)


@router.get("/{antimicrobial_id}", response_model=AntimicrobialOut)
def get_antimicrobial(antimicrobial_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    record = antimicrobial_service.get_antimicrobial(db, antimicrobial_id)
    if not record:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Antimicrobial not found")
    return record


@router.get("/", response_model=list[AntimicrobialOut])
def list_antimicrobials(
    drug_class: str | None = None,
    active_only: bool = False,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return antimicrobial_service.list_antimicrobials(db, drug_class, active_only, skip, limit)


@router.put("/{antimicrobial_id}", response_model=AntimicrobialOut)
def update_antimicrobial(
    antimicrobial_id: int,
    data: AntimicrobialUpdate,
    db: Session = Depends(get_db),
    user:User=Depends(get_current_user),
):
    record = antimicrobial_service.update_antimicrobial(db, antimicrobial_id, data)
    if not record:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Antimicrobial not found")
    return record


@router.delete("/{antimicrobial_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_antimicrobial(
    antimicrobial_id: int,
    db: Session = Depends(get_db),
    user:User=Depends(get_current_user),
):
    if not antimicrobial_service.delete_antimicrobial(db, antimicrobial_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Antimicrobial not found")