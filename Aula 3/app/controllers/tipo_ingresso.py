from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.services import tipo_ingresso as servico
from app.views.comuns import TipoSala
from app.views.tipo_ingresso import TipoIngressoCreate, TipoIngressoOut, TipoIngressoUpdate

router = APIRouter(prefix="/tipos-ingresso", tags=["Tipos de ingresso"])


@router.get("", response_model=list[TipoIngressoOut],
            summary="Lista a tabela de precos por tipo de sala")
def listar(db: Session = Depends(get_db)):
    return servico.listar(db)


@router.get("/{tipo_sala}", response_model=TipoIngressoOut, summary="Detalha um tipo de ingresso")
def buscar(tipo_sala: TipoSala, db: Session = Depends(get_db)):
    return servico.buscar(db, tipo_sala)


@router.post("", response_model=TipoIngressoOut, status_code=status.HTTP_201_CREATED,
             summary="Cadastra o valor do ingresso de um tipo de sala")
def criar(dados: TipoIngressoCreate, db: Session = Depends(get_db)):
    return servico.criar(db, dados)


@router.put("/{tipo_sala}", response_model=TipoIngressoOut, summary="Edita o valor do ingresso")
def atualizar(tipo_sala: TipoSala, dados: TipoIngressoUpdate, db: Session = Depends(get_db)):
    return servico.atualizar(db, tipo_sala, dados)


@router.delete("/{tipo_sala}", status_code=status.HTTP_204_NO_CONTENT,
               summary="Remove o valor do ingresso")
def remover(tipo_sala: TipoSala, db: Session = Depends(get_db)):
    servico.remover(db, tipo_sala)
