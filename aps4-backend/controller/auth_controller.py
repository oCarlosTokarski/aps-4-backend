from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from schema.usuario_schema import LoginRequest, Token, UsuarioResposta
from security.security import get_usuario_atual
from service import auth_service


router = APIRouter(
    prefix="/auth",
    tags=["Autenticação"]
)


@router.post(
    "/login",
    response_model=Token
)
def login(dados: LoginRequest, db: Session = Depends(get_db)):
    return auth_service.login(db, dados)


@router.get(
    "/me",
    response_model=UsuarioResposta
)
def consultar_meus_dados(usuario=Depends(get_usuario_atual)):
    return usuario
