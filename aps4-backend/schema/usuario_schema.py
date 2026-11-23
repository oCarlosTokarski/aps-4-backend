from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class UsuarioCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    nome: str = Field(..., min_length=1)
    email: EmailStr
    senha: str = Field(..., min_length=8)

    @field_validator("nome")
    def nome_nao_vazio(cls, valor):
        valor = valor.strip()
        if valor == "":
            raise ValueError("O nome não pode ser vazio.")
        return valor


class UsuarioResposta(BaseModel):
    id: int
    nome: str
    email: EmailStr
    perfil: str

    model_config = ConfigDict(from_attributes=True)


class LoginRequest(BaseModel):
    email: EmailStr
    senha: str = Field(..., min_length=1)


class Token(BaseModel):
    access_token: str
    token_type: str
