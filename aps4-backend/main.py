from fastapi import FastAPI

from database import Base, SessionLocal, engine
from controller.evento_controller import router as evento_router
from controller.participante_controller import router as participante_router
from controller.inscricao_controller import router as inscricao_router
from controller.relatorio_controller import router as relatorio_router
from controller.usuario_controller import router as usuario_router
from controller.auth_controller import router as auth_router
from service import usuario_service

from model import evento, participante, inscricao, usuario

Base.metadata.create_all(bind=engine)

with SessionLocal() as db:
    usuario_service.criar_admin_inicial(db)

app = FastAPI(
    title="API de Eventos Acadêmicos",
    description="API RESTful para gerenciamento de eventos e participantes.",
    version="4.0.0"
)

app.include_router(evento_router)
app.include_router(participante_router)
app.include_router(inscricao_router)
app.include_router(relatorio_router)
app.include_router(usuario_router)
app.include_router(auth_router)
