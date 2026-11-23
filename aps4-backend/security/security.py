import os
from datetime import datetime, timedelta, timezone

import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pwdlib import PasswordHash

from database import get_db
from model.usuario import Usuario


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
EXPIRACAO_MINUTOS = int(os.getenv("TOKEN_EXPIRACAO_MINUTOS", "30"))

if not SECRET_KEY:
    raise RuntimeError(
        "Defina a variável SECRET_KEY no arquivo .env (veja o README)."
    )

PERFIL_ADMIN = "administrador"
PERFIL_USUARIO = "usuario"

password_hash = PasswordHash.recommended()

esquema_bearer = HTTPBearer(auto_error=False)


def gerar_hash_senha(senha: str) -> str:
    return password_hash.hash(senha)


def verificar_senha(senha: str, senha_hash: str) -> bool:
    return password_hash.verify(senha, senha_hash)


def criar_token(usuario_id: int) -> str:
    expiracao = datetime.now(timezone.utc) + timedelta(
        minutes=EXPIRACAO_MINUTOS
    )

    dados = {
        "sub": str(usuario_id),
        "exp": expiracao
    }

    return jwt.encode(dados, SECRET_KEY, algorithm=ALGORITHM)


def get_usuario_atual(
    credenciais: HTTPAuthorizationCredentials = Depends(esquema_bearer),
    db=Depends(get_db)
):
    erro = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais.",
        headers={"WWW-Authenticate": "Bearer"}
    )

    if credenciais is None:
        raise erro

    try:
        dados = jwt.decode(
            credenciais.credentials,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            options={"require": ["exp", "sub"]}
        )
        usuario_id = int(dados["sub"])
    except (jwt.PyJWTError, ValueError):
        raise erro

    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()

    if usuario is None:
        raise erro

    return usuario


def exigir_admin(usuario: Usuario = Depends(get_usuario_atual)):
    if usuario.perfil != PERFIL_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não possui permissão para executar esta operação."
        )

    return usuario
