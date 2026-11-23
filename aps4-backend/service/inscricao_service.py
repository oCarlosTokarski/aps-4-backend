from fastapi import HTTPException, status

from database import salvar
from model.inscricao import Inscricao
from service.evento_service import buscar_evento
from service.participante_service import buscar_participante


def inscrever_participante(db, evento_id: int, participante_id: int):
    evento = buscar_evento(db, evento_id)
    participante = buscar_participante(db, participante_id)

    ja_inscrito = (
        db.query(Inscricao)
        .filter(
            Inscricao.evento_id == evento.id,
            Inscricao.participante_id == participante.id
        )
        .first()
    )

    if ja_inscrito is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Participante já está inscrito neste evento."
        )

    if len(evento.inscricoes) >= evento.capacidade:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Não existem vagas disponíveis para este evento."
        )

    inscricao = Inscricao(evento_id=evento.id, participante_id=participante.id)

    db.add(inscricao)
    salvar(db)
    db.refresh(inscricao)

    return inscricao


def listar_inscritos(db, evento_id: int):
    evento = buscar_evento(db, evento_id)

    return [inscricao.participante for inscricao in evento.inscricoes]
