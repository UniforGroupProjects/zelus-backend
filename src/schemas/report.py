from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# 1. Definição básica 
class ReportBase(BaseModel):
    title: str
    description: str
    category: str
    latitude: float
    longitude: float
    image_url: Optional[str] = None 

# 2. O que o usuário envia (Request)
class ReportCreate(ReportBase):
    pass

# 3. O que a API devolve (Response) 
class ReportResponse(ReportBase):
    id: int
    status: str = "Aberto"
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# 4. O que o usuário envia para editar 
class ReportUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    status: Optional[str] = None
    image_url: Optional[str] = None