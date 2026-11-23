from fastapi import HTTPException, status

from database import salvar
from model.participante import Participante
from schema.participante_schema import ParticipanteBase


def verificar_email_duplicado(db, email: str, participante_id: int = None):
    consulta = db.query(Participante).filter(Participante.email == email)

    # Na atualização, ignora o próprio participante
    if participante_id is not None:
        consulta = consulta.filter(Participante.id != participante_id)

    if consulta.first() is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Já existe um participante cadastrado com este e-mail."
        )


def criar_participante(db, dados: ParticipanteBase):
    verificar_email_duplicado(db, dados.email)

    participante = Participante(**dados.model_dump())

    db.add(participante)
    salvar(db)
    db.refresh(participante)

    return participante


def listar_participantes(db):
    return db.query(Participante).all()


def buscar_participante(db, participante_id: int):
    participante = (
        db.query(Participante)
        .filter(Participante.id == participante_id)
        .first()
    )

    if participante is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Participante não encontrado."
        )

    return participante


def atualizar_participante(
    db,
    participante_id: int,
    dados: ParticipanteBase
):
    participante = buscar_participante(db, participante_id)

    verificar_email_duplicado(db, dados.email, participante_id)

    participante.nome = dados.nome
    participante.email = dados.email
    participante.curso = dados.curso

    salvar(db)
    db.refresh(participante)

    return participante


def excluir_participante(db, participante_id: int):
    participante = buscar_participante(db, participante_id)

    db.delete(participante)
    salvar(db)
