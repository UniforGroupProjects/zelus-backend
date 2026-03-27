from sqlalchemy.orm import Session
from src.models.report import Report
from src.schemas.report import ReportCreate

def create_report(db: Session, report_data: ReportCreate, user_id: int):
    # Criamos o objeto associando ao ID do usuário autenticado
    db_report = Report(
        **report_data.model_dump(),
        user_id=user_id,
        status="open" 
    )
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report

def get_report_by_id(db: Session, report_id: int):
    return db.query(Report).filter(Report.id == report_id).first()

def get_all_reports(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Report).offset(skip).limit(limit).all()

def get_my_reports(db: Session, user_id: int):
    """Business Logic: Buscar apenas as denúncias do usuário logado"""
    return db.query(Report).filter(Report.user_id == user_id).all()

def delete_report(db: Session, report_id: int, user_id: int):
    # 1. Busca a denúncia no banco
    db_report = db.query(Report).filter(Report.id == report_id).first()
    
    # 2. Se não existir, avisa (retornando None)
    if not db_report:
        return None
    
    # 3. SEGURANÇA: Se o dono da denúncia não for quem está logado, dá erro!
    if db_report.user_id != user_id:
        return "not_authorized"

    # 4. Se passou pelos testes, deleta de verdade
    db.delete(db_report)
    db.commit()
    return True