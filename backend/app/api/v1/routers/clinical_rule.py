from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.clinical_rule import ClinicalRuleCreate, ClinicalRuleUpdate, ClinicalRuleOut
from app.services import clinical_rule_service
from app.auth.auth import  get_current_user
from app.models.user import UserRole

router = APIRouter(prefix="/clinical-rules", tags=["Clinical Rules"])


@router.post("/", response_model=ClinicalRuleOut, status_code=status.HTTP_201_CREATED)
def create_rule(
    data: ClinicalRuleCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return clinical_rule_service.create_rule(db, data)


@router.get("/{rule_id}", response_model=ClinicalRuleOut)
def get_rule(rule_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return clinical_rule_service.get_rule(db, rule_id)


@router.get("/", response_model=list[ClinicalRuleOut])
def list_rules(
    active_only: bool = False,
    pathogen_id: int | None = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return clinical_rule_service.list_rules(db, active_only, pathogen_id, skip, limit)


@router.put("/{rule_id}", response_model=ClinicalRuleOut)
def update_rule(
    rule_id: int,
    data: ClinicalRuleUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return clinical_rule_service.update_rule(db, rule_id, data)


@router.patch("/{rule_id}/deactivate", response_model=ClinicalRuleOut)
def deactivate_rule(
    rule_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return clinical_rule_service.deactivate_rule(db, rule_id)


@router.delete("/{rule_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_rule(
    rule_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    if not clinical_rule_service.delete_rule(db, rule_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Rule not found")