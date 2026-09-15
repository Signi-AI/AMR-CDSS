from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.cell_count import CellCountCreate, CellCountOut
from app.services import cell_count_service
from app.auth.auth import get_current_user
from app.models.user import UserRole

router = APIRouter(prefix="/cell-counts", tags=["Cell Counts"])


@router.post("/", response_model=CellCountOut, status_code=status.HTTP_201_CREATED)
def create_cell_count(
    analysis_result_id,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return cell_count_service.create_cell_count(db,analysis_result_id)


@router.get("/{cell_count_id}", response_model=CellCountOut)
def get_cell_count(cell_count_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return cell_count_service.get_cell_count(db, cell_count_id)


@router.get("/by-analysis/{analysis_result_id}", response_model=list[CellCountOut])
def get_by_analysis_result(analysis_result_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return cell_count_service.get_by_analysis_result(db, analysis_result_id)


@router.delete("/{cell_count_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cell_count(
    cell_count_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    if not cell_count_service.delete_cell_count(db, cell_count_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Cell count not found")