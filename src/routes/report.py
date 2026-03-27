from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

# Importações de conexão e lógica
from src.database import get_db
from src.schemas.report import ReportCreate, ReportResponse, ReportUpdate
from src.services import report as report_service

# Importação da segurança (que está na raiz)
from src.auth_utils import get_current_user_id 

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.post("/", response_model=ReportResponse, status_code=status.HTTP_201_CREATED)
def create_new_report(
    report_data: ReportCreate, 
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id) # Extrai o ID do Token
):
    """
    Cria uma nova denúncia. 
    O 'user_id' é preenchido automaticamente pelo sistema através do Token JWT.
    """
    return report_service.create_report(
        db=db, 
        report_data=report_data, 
        user_id=current_user_id
    )

@router.get("/", response_model=List[ReportResponse])
def list_all_reports(db: Session = Depends(get_db)):
    """
    Lista todas as denúncias registradas no sistema (Público para o Mapa).
    """
    return report_service.get_all_reports(db)

@router.get("/me", response_model=List[ReportResponse])
def list_my_reports(
    db: Session = Depends(get_db), 
    current_user_id: int = Depends(get_current_user_id)
):
    """
    Retorna apenas as denúncias feitas pelo usuário logado.
    """
    return report_service.get_my_reports(db, user_id=current_user_id)

@router.get("/{report_id}", response_model=ReportResponse)
def read_report(report_id: int, db: Session = Depends(get_db)):
    """
    Busca os detalhes de uma denúncia específica pelo ID.
    """
    db_report = report_service.get_report_by_id(db, report_id=report_id)
    if db_report is None:
        raise HTTPException(status_code=404, detail="Denúncia não encontrada")
    return db_report

@router.delete("/{report_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_report(
    report_id: int, 
    db: Session = Depends(get_db), 
    current_user_id: int = Depends(get_current_user_id)
):
    success = report_service.delete_report(db, report_id, user_id=current_user_id)
    
    if success is None:
        raise HTTPException(status_code=404, detail="Denúncia não encontrada")
    
    if success == "not_authorized":
        raise HTTPException(
            status_code=403, 
            detail="Você não tem permissão para apagar uma denúncia que não é sua!"
        )
    
    return None 

@router.patch("/{report_id}", response_model=ReportResponse)
def update_existing_report(
    report_id: int,
    report_data: ReportUpdate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    Atualiza uma denúncia existente. 
    Apenas os campos enviados serão alterados (PATCH).
    """
    updated_report = report_service.update_report(
        db=db, 
        report_id=report_id, 
        user_id=current_user_id, 
        report_data=report_data
    )
    
    if updated_report is None:
        raise HTTPException(status_code=404, detail="Denúncia não encontrada")
        
    if updated_report == "not_authorized":
        raise HTTPException(
            status_code=403, 
            detail="Você não tem permissão para editar uma denúncia que não é sua!"
        )
        
    return updated_report