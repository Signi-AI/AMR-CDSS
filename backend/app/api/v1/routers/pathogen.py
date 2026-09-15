from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.pathogen import PathogenCreate, PathogenUpdate, PathogenOut
from app.services import pathogen_service
from app.auth.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/pathogens", tags=["Pathogens"])


@router.post("/", response_model=PathogenOut, status_code=status.HTTP_201_CREATED)
def create_pathogen(
    data: PathogenCreate,
    db: Session = Depends(get_db),
    user:User=Depends(get_current_user),
):
    if pathogen_service.get_by_name(db, data.name):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Pathogen with this name already exists")
    return pathogen_service.create_pathogen(db, data)


@router.get("/{pathogen_id}", response_model=PathogenOut)
def get_pathogen(pathogen_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    record = pathogen_service.get_pathogen(db, pathogen_id)
    if not record:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Pathogen not found")
    return record


@router.get("/", response_model=list[PathogenOut])
def list_pathogens(
    family: str | None = None,
    active_only: bool = False,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return pathogen_service.list_pathogens(db, family, active_only, skip, limit)


@router.put("/{pathogen_id}", response_model=PathogenOut)
def update_pathogen(
    pathogen_id: int,
    data: PathogenUpdate,
    db: Session = Depends(get_db),
    user:User=Depends(get_current_user),
):
    record = pathogen_service.update_pathogen(db, pathogen_id, data)
    if not record:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Pathogen not found")
    return record


@router.delete("/{pathogen_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pathogen(
    pathogen_id: int,
    db: Session = Depends(get_db),
    user:User=Depends(get_current_user),
):
    if not pathogen_service.delete_pathogen(db, pathogen_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Pathogen not found")