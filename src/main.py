from fastapi import FastAPI
# 1. Adicionamos 'auth' aqui na lista de importação
from src.routes import auth, report, user 
from src.database import engine, Base
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Zelus API")

# 1. Criamos o banco
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Erro ao conectar no banco: {e}", flush=True)

# 2. Adicionamos a segurança
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Em produção, coloque o endereço do seu front
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# 3. Registramos as rotas. A de auth (login) é bom ficar em primeiro!
app.include_router(auth.router)
app.include_router(report.router)
app.include_router(user.router)


@app.get("/")
def home():
    return {"message": "Zelus API rodando na pasta src!"}