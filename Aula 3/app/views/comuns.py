from datetime import date, datetime
from typing import Annotated, Literal

from pydantic import BeforeValidator, PlainSerializer

FORMATO_DATA = "%d/%m/%Y"

TipoSala = Literal["2D", "3D"]


def _para_data(valor: object) -> date:
    if isinstance(valor, date) and not isinstance(valor, datetime):
        return valor
    if not isinstance(valor, str):
        raise ValueError("a data deve ser um texto no formato DD/MM/AAAA")
    try:
        return datetime.strptime(valor.strip(), FORMATO_DATA).date()
    except ValueError:
        raise ValueError("data invalida: use o formato DD/MM/AAAA") from None


def _texto_limpo(valor: object) -> object:
    return valor.strip() if isinstance(valor, str) else valor


DataBR = Annotated[
    date,
    BeforeValidator(_para_data),
    PlainSerializer(lambda d: d.strftime(FORMATO_DATA), return_type=str, when_used="json"),
]

TextoLimpo = Annotated[str, BeforeValidator(_texto_limpo)]
