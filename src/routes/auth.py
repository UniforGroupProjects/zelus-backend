from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.database import get_db
from src import models, auth_utils

router = APIRouter(tags=["Authentication"])

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # 1. Procura o usuário pelo e-mail
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    
    # 2. Se não achar ou a senha não bater... Erro!
    if not user or not auth_utils.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="E-mail ou senha incorretos")

    # 3. Se deu certo, dá o crachá (Token)
    token = auth_utils.create_access_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}