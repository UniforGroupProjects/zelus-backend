from fastapi import FastAPI
from src.routes import auth, report, user 
from src.database import engine, Base
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Zelus API")

try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Erro ao conectar no banco: {e}", flush=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.router)
app.include_router(report.router)
app.include_router(user.router)


from fastapi.responses import HTMLResponse

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def home():
    return """
    <html>
        <head>
            <title>Zelus API</title>
            <style>
                body { font-family: sans-serif; background: #1a1a1a; color: #eee; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
                .card { border: 1px solid #333; padding: 2rem; border-radius: 8px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
                a { color: #00ffcc; text-decoration: none; font-weight: bold; }
                .status { color: #00ff00; font-size: 0.9rem; }
            </style>
        </head>
        <body>
            <div class="card">
                <h1>Zelus API <span class="status">● Online</span></h1>
                <p>Sistema de Gerenciamento de Manutenção Urbana</p>
                <p>Acesse a <a href="/docs">Documentação Interativa</a> para começar.</p>
            </div>
        </body>
    </html>
    """