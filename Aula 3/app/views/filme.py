from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.views.comuns import DataBR, TextoLimpo


class FilmeBase(BaseModel):
    nome: Annotated[TextoLimpo, Field(min_length=1, examples=["Nome do filme"])]
    data_estreia: Annotated[DataBR, Field(examples=["01/03/2026"])]
    data_saida: Annotated[DataBR, Field(examples=["30/04/2026"])]
    duracao: Annotated[int, Field(gt=0, description="Duracao em minutos", examples=[155])]

    @model_validator(mode="after")
    def _estreia_antes_da_saida(self):
        if self.data_estreia > self.data_saida:
            raise ValueError("data_estreia deve ser anterior ou igual a data_saida")
        return self


class FilmeCreate(FilmeBase):
    pass


class FilmeUpdate(FilmeBase):
    pass


class FilmeOut(FilmeBase):
    model_config = ConfigDict(from_attributes=True)

    codigo: int
