from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError

# Configuração básica de segurança
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "sua_chave_secreta_muito_longa_aqui" 
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login") # "login" deve ser a rota de 

def get_password_hash(password: str):
    """Transforma senha em código secreto"""
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    """Compara a senha digitada com a do banco"""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    """Cria o 'crachá' (Token) para o usuário"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30) # O login vale por 30 min
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user_id(token: str = Depends(oauth2_scheme)):
    """Lê o token, valida e retorna o ID do usuário"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub") # O 'sub' é o padrão para o ID do usuário
        if user_id is None:
            raise credentials_exception
        return int(user_id)
    except (JWTError, ValueError):
            raise credentials_exception