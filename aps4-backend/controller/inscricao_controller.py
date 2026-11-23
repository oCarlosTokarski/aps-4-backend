from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from schema.inscricao_schema import Inscricao
from schema.participante_schema import Participante
from security.security import exigir_admin, get_usuario_atual
from service import inscricao_service


router = APIRouter(
    prefix="/eventos",
    tags=["Inscrições"]
)


@router.post(
    "/{evento_id}/inscricoes/{participante_id}",
    response_model=Inscricao,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_usuario_atual)]
)
def realizar_inscricao(
    evento_id: int,
    participante_id: int,
    db: Session = Depends(get_db)
):
    return inscricao_service.inscrever_participante(
        db,
        evento_id,
        participante_id
    )


@router.get(
    "/{evento_id}/inscricoes",
    response_model=list[Participante],
    dependencies=[Depends(exigir_admin)]
)
def consultar_inscritos(evento_id: int, db: Session = Depends(get_db)):
    return inscricao_service.listar_inscritos(db, evento_id)
