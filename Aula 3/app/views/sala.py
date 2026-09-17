from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

from app.views.comuns import TipoSala


class SalaBase(BaseModel):
    capacidade: Annotated[int, Field(gt=0, examples=[50])]
    tipo: Annotated[TipoSala, Field(examples=["2D"])]


class SalaCreate(SalaBase):
    numero: Annotated[int, Field(gt=0, examples=[1])]


class SalaUpdate(SalaBase):
    pass


class SalaOut(SalaBase):
    model_config = ConfigDict(from_attributes=True)

    numero: int
