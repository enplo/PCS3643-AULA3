from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import TipoIngresso
from app.services.erros import Conflito, NaoEncontrado
from app.views.tipo_ingresso import TipoIngressoCreate, TipoIngressoUpdate


def listar(db: Session) -> list[TipoIngresso]:
    return list(db.scalars(select(TipoIngresso).order_by(TipoIngresso.tipo_sala)))


def buscar(db: Session, tipo_sala: str) -> TipoIngresso:
    tipo = db.get(TipoIngresso, tipo_sala)
    if tipo is None:
        raise NaoEncontrado(f"Nao ha valor de ingresso cadastrado para salas {tipo_sala}.")
    return tipo


def criar(db: Session, dados: TipoIngressoCreate) -> TipoIngresso:
    if db.get(TipoIngresso, dados.tipo_sala) is not None:
        raise Conflito(
            f"Ja existe valor cadastrado para salas {dados.tipo_sala}. Use PUT para altera-lo."
        )
    tipo = TipoIngresso(**dados.model_dump())
    db.add(tipo)
    db.commit()
    db.refresh(tipo)
    return tipo


def atualizar(db: Session, tipo_sala: str, dados: TipoIngressoUpdate) -> TipoIngresso:
    tipo = buscar(db, tipo_sala)
    tipo.valor = dados.valor
    db.commit()
    db.refresh(tipo)
    return tipo


def remover(db: Session, tipo_sala: str) -> None:
    tipo = buscar(db, tipo_sala)
    db.delete(tipo)
    db.commit()
