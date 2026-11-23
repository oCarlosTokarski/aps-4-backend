import os

from fastapi import HTTPException, status

from database import salvar
from model.usuario import Usuario
from schema.usuario_schema import UsuarioCreate
from security.security import PERFIL_ADMIN, PERFIL_USUARIO, gerar_hash_senha


def buscar_por_email(db, email: str):
    return db.query(Usuario).filter(Usuario.email == email).first()


def criar_usuario(db, dados: UsuarioCreate, perfil: str = PERFIL_USUARIO):
    if buscar_por_email(db, dados.email) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Já existe um usuário cadastrado com este e-mail."
        )

    usuario = Usuario(
        nome=dados.nome,
        email=dados.email,
        senha_hash=gerar_hash_senha(dados.senha),
        perfil=perfil
    )

    db.add(usuario)
    salvar(db)
    db.refresh(usuario)

    return usuario


def criar_admin_inicial(db):
    email = os.getenv("ADMIN_EMAIL")
    senha = os.getenv("ADMIN_SENHA")
    nome = os.getenv("ADMIN_NOME", "Administrador")

    if not email or not senha:
        return

    if buscar_por_email(db, email) is not None:
        return

    dados = UsuarioCreate(nome=nome, email=email, senha=senha)
    criar_usuario(db, dados, PERFIL_ADMIN)
