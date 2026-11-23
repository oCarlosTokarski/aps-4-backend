from fastapi import HTTPException, status

from schema.usuario_schema import LoginRequest
from security.security import criar_token, verificar_senha
from service.usuario_service import buscar_por_email


def login(db, dados: LoginRequest):
    usuario = buscar_por_email(db, dados.email)

    if usuario is None or not verificar_senha(dados.senha, usuario.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha inválidos.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return {
        "access_token": criar_token(usuario.id),
        "token_type": "bearer"
    }
