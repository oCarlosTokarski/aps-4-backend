from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ParticipanteBase(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    nome: str = Field(..., min_length=1)
    email: EmailStr
    curso: str = Field(..., min_length=1)


class Participante(ParticipanteBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
