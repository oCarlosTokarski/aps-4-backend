from fastapi import HTTPException, status

from database import salvar
from model.evento import Evento
from schema.evento_schema import EventoBase


def criar_evento(db, dados: EventoBase):
    evento = Evento(**dados.model_dump())

    db.add(evento)
    salvar(db)
    db.refresh(evento)

    return evento


def listar_eventos(db):
    return db.query(Evento).all()


def buscar_evento(db, evento_id: int):
    evento = db.query(Evento).filter(Evento.id == evento_id).first()

    if evento is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento não encontrado."
        )

    return evento


def atualizar_evento(db, evento_id: int, dados: EventoBase):
    evento = buscar_evento(db, evento_id)

    if dados.capacidade < len(evento.inscricoes):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A capacidade não pode ser menor que o número de inscritos."
        )

    evento.titulo = dados.titulo
    evento.descricao = dados.descricao
    evento.data = dados.data
    evento.horario = dados.horario
    evento.local = dados.local
    evento.capacidade = dados.capacidade
    evento.categoria = dados.categoria

    salvar(db)
    db.refresh(evento)

    return evento


def excluir_evento(db, evento_id: int):
    evento = buscar_evento(db, evento_id)

    db.delete(evento)
    salvar(db)
