from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.services import sessao as servico
from app.views.comuns import DataBR
from app.views.sessao import SessaoCreate, SessaoOut, SessaoUpdate

router = APIRouter(prefix="/sessoes", tags=["Sessoes"])


@router.get("", response_model=list[SessaoOut],
            summary="Lista as sessoes, opcionalmente filtrando por data")
def listar(
    db: Session = Depends(get_db),
    data: Annotated[
        DataBR | None,
        Query(description="Filtra por data, no formato DD/MM/AAAA", examples=["15/03/2026"]),
    ] = None,
):
    return servico.listar(db, data)


@router.get("/{codigo}", response_model=SessaoOut, summary="Detalha uma sessao")
def buscar(codigo: int, db: Session = Depends(get_db)):
    return servico.buscar(db, codigo)


@router.post("", response_model=SessaoOut, status_code=status.HTTP_201_CREATED,
             summary="Cadastra uma sessao")
def criar(dados: SessaoCreate, db: Session = Depends(get_db)):
    return servico.criar(db, dados)


@router.put("/{codigo}", response_model=SessaoOut, summary="Edita uma sessao")
def atualizar(codigo: int, dados: SessaoUpdate, db: Session = Depends(get_db)):
    return servico.atualizar(db, codigo, dados)


@router.delete("/{codigo}", status_code=status.HTTP_204_NO_CONTENT,
               summary="Remove uma sessao")
def remover(codigo: int, db: Session = Depends(get_db)):
    servico.remover(db, codigo)
