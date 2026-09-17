from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

from app.views.comuns import TipoSala


class TipoIngressoBase(BaseModel):
    valor: Annotated[int, Field(gt=0, description="Valor da inteira, em reais", examples=[30])]


class TipoIngressoCreate(TipoIngressoBase):
    tipo_sala: Annotated[TipoSala, Field(examples=["3D"])]


class TipoIngressoUpdate(TipoIngressoBase):
    pass


class TipoIngressoOut(TipoIngressoBase):
    model_config = ConfigDict(from_attributes=True)

    tipo_sala: str
