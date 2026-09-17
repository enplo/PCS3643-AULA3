from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.services import sala as servico
from app.views.sala import SalaCreate, SalaOut, SalaUpdate

router = APIRouter(prefix="/salas", tags=["Salas"])


@router.get("", response_model=list[SalaOut], summary="Lista todas as salas")
def listar(db: Session = Depends(get_db)):
    return servico.listar(db)


@router.get("/{numero}", response_model=SalaOut, summary="Detalha uma sala")
def buscar(numero: int, db: Session = Depends(get_db)):
    return servico.buscar(db, numero)


@router.post("", response_model=SalaOut, status_code=status.HTTP_201_CREATED,
             summary="Cadastra uma sala")
def criar(dados: SalaCreate, db: Session = Depends(get_db)):
    return servico.criar(db, dados)


@router.put("/{numero}", response_model=SalaOut, summary="Edita uma sala")
def atualizar(numero: int, dados: SalaUpdate, db: Session = Depends(get_db)):
    return servico.atualizar(db, numero, dados)


@router.delete("/{numero}", status_code=status.HTTP_204_NO_CONTENT,
               summary="Remove uma sala")
def remover(numero: int, db: Session = Depends(get_db)):
    servico.remover(db, numero)
