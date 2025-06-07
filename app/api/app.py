from fastapi import FastAPI, Request, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse
from pathlib import Path
from app.api.database import init_db
from app.api.routes import api_router
from app.api.core.security import verify_session
import os

app = FastAPI(
    title="Recomienda App API",
    description="API para la aplicación de recomendaciones de lugares",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # expose_headers=["Set-Cookie"]
)

# Configurar archivos estáticos
app.mount("/static", StaticFiles(directory="../frontend-ui"), name="static")

# Incluir el router principal
app.include_router(api_router)

# Eventos de inicio y cierre
@app.on_event("startup")
async def startup_event():
    await init_db()

@app.on_event("shutdown")
async def shutdown_event():
    pass