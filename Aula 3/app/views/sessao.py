from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

from app.views.comuns import DataBR


class SessaoBase(BaseModel):
    sala_numero: Annotated[int, Field(gt=0, examples=[1])]
    filme_codigo: Annotated[int, Field(gt=0, examples=[1])]
    data: Annotated[DataBR, Field(examples=["15/03/2026"])]
    hora_inicio: Annotated[int, Field(ge=0, le=23, examples=[20])]


class SessaoCreate(SessaoBase):
    pass


class SessaoUpdate(SessaoBase):
    pass


class SessaoOut(SessaoBase):
    model_config = ConfigDict(from_attributes=True)

    codigo: int
    capacidade: int
    assentos_livres: int
