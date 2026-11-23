from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from database import get_db
from schema.evento_schema import Evento, EventoBase
from security.security import exigir_admin
from service import evento_service


router = APIRouter(
    prefix="/eventos",
    tags=["Eventos"]
)


@router.post(
    "",
    response_model=Evento,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(exigir_admin)]
)
def cadastrar_evento(dados: EventoBase, db: Session = Depends(get_db)):
    return evento_service.criar_evento(db, dados)


@router.get(
    "",
    response_model=list[Evento]
)
def listar_eventos(db: Session = Depends(get_db)):
    return evento_service.listar_eventos(db)


@router.get(
    "/{evento_id}",
    response_model=Evento
)
def consultar_evento(evento_id: int, db: Session = Depends(get_db)):
    return evento_service.buscar_evento(db, evento_id)


@router.put(
    "/{evento_id}",
    response_model=Evento,
    dependencies=[Depends(exigir_admin)]
)
def atualizar_evento(
    evento_id: int,
    dados: EventoBase,
    db: Session = Depends(get_db)
):
    return evento_service.atualizar_evento(db, evento_id, dados)


@router.delete(
    "/{evento_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(exigir_admin)]
)
def excluir_evento(evento_id: int, db: Session = Depends(get_db)):
    evento_service.excluir_evento(db, evento_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
