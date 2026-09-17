from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Assento, Filme, Sala, Sessao
from app.services.erros import Conflito, NaoEncontrado
from app.views.sessao import SessaoCreate, SessaoUpdate


def listar(db: Session, data: date | None = None) -> list[Sessao]:
    consulta = select(Sessao).order_by(Sessao.codigo)
    if data is not None:
        consulta = consulta.where(Sessao.data == data)
    return list(db.scalars(consulta))


def buscar(db: Session, codigo: int) -> Sessao:
    sessao = db.get(Sessao, codigo)
    if sessao is None:
        raise NaoEncontrado(f"Sessao de codigo {codigo} nao encontrada.")
    return sessao


def _exigir_sala(db: Session, numero: int) -> Sala:
    sala = db.get(Sala, numero)
    if sala is None:
        raise NaoEncontrado(f"Sala de numero {numero} nao encontrada.")
    return sala


def _exigir_filme(db: Session, codigo: int) -> Filme:
    filme = db.get(Filme, codigo)
    if filme is None:
        raise NaoEncontrado(f"Filme de codigo {codigo} nao encontrado.")
    return filme


def _garantir_horario_livre(
    db: Session,
    sala_numero: int,
    data: date,
    hora_inicio: int,
    ignorar: int | None = None,
) -> None:
    consulta = select(Sessao).where(
        Sessao.sala_numero == sala_numero,
        Sessao.data == data,
        Sessao.hora_inicio == hora_inicio,
    )
    if ignorar is not None:
        consulta = consulta.where(Sessao.codigo != ignorar)
    if db.scalar(consulta) is not None:
        raise Conflito(
            f"A sala {sala_numero} ja tem sessao em {data.strftime('%d/%m/%Y')} as {hora_inicio}h."
        )


def criar(db: Session, dados: SessaoCreate) -> Sessao:
    sala = _exigir_sala(db, dados.sala_numero)
    _exigir_filme(db, dados.filme_codigo)
    _garantir_horario_livre(db, dados.sala_numero, dados.data, dados.hora_inicio)

    sessao = Sessao(**dados.model_dump())
    sessao.assentos = [
        Assento(numero=numero, ocupado=False) for numero in range(1, sala.capacidade + 1)
    ]
    db.add(sessao)
    db.commit()
    db.refresh(sessao)
    return sessao


def atualizar(db: Session, codigo: int, dados: SessaoUpdate) -> Sessao:
    sessao = buscar(db, codigo)
    nova_sala = _exigir_sala(db, dados.sala_numero)
    _exigir_filme(db, dados.filme_codigo)
    _garantir_horario_livre(
        db, dados.sala_numero, dados.data, dados.hora_inicio, ignorar=codigo
    )

    trocou_de_sala = dados.sala_numero != sessao.sala_numero
    if trocou_de_sala and sessao.tem_ingresso_vendido:
        raise Conflito(
            f"A sessao {codigo} ja tem ingresso vendido e por isso nao pode mudar de sala."
        )

    for campo, valor in dados.model_dump().items():
        setattr(sessao, campo, valor)

    if trocou_de_sala:
        sessao.assentos = [
            Assento(numero=numero, ocupado=False)
            for numero in range(1, nova_sala.capacidade + 1)
        ]

    db.commit()
    db.refresh(sessao)
    return sessao


def remover(db: Session, codigo: int) -> None:
    sessao = buscar(db, codigo)
    if sessao.tem_ingresso_vendido:
        raise Conflito(
            f"A sessao {codigo} ja tem ingresso vendido e por isso nao pode ser removida."
        )
    db.delete(sessao)
    db.commit()
