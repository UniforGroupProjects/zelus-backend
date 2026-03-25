from fastapi import FastAPI
# 1. Adicionamos 'auth' aqui na lista de importação
from src.routes import auth, items, report, user 
from src.database import engine, Base

app = FastAPI(title="Zelus API")

print("--- Verificando Banco de Dados ---", flush=True)
try:
    # Força a criação das tabelas no banco de dados
    Base.metadata.create_all(bind=engine)
    print("Tabelas verificadas/criadas com sucesso!", flush=True)
except Exception as e:
    print(f"Erro ao conectar no banco: {e}", flush=True)

# 2. Registramos as rotas. A de auth (login) é bom ficar em primeiro!
app.include_router(auth.router)
app.include_router(items.router)
app.include_router(report.router)
app.include_router(user.router)

@app.get("/")
def home():
    return {"message": "Zelus API rodando na pasta src!"}