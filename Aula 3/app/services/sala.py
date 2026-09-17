from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Assento, Sala
from app.services.erros import Conflito, NaoEncontrado
from app.views.sala import SalaCreate, SalaUpdate


def listar(db: Session) -> list[Sala]:
    return list(db.scalars(select(Sala).order_by(Sala.numero)))


def buscar(db: Session, numero: int) -> Sala:
    sala = db.get(Sala, numero)
    if sala is None:
        raise NaoEncontrado(f"Sala de numero {numero} nao encontrada.")
    return sala


def criar(db: Session, dados: SalaCreate) -> Sala:
    if db.get(Sala, dados.numero) is not None:
        raise Conflito(f"Ja existe uma sala de numero {dados.numero}.")
    sala = Sala(**dados.model_dump())
    db.add(sala)
    db.commit()
    db.refresh(sala)
    return sala


def _ajustar_assentos(sala: Sala, nova_capacidade: int) -> None:
    """Redimensiona o mapa de assentos das sessoes ja cadastradas na sala.

    Crescer e sempre seguro. Encolher so e permitido se nenhum dos assentos
    que sairiam do mapa tiver ingresso vendido.
    """
    for sessao in sala.sessoes:
        excedentes = [a for a in sessao.assentos if a.numero > nova_capacidade]
        vendidos = sorted(a.numero for a in excedentes if a.ocupado)
        if vendidos:
            raise Conflito(
                f"A sessao {sessao.codigo} tem ingresso vendido nos assentos {vendidos}, "
                f"que deixariam de existir com capacidade {nova_capacidade}."
            )
        for assento in excedentes:
            sessao.assentos.remove(assento)

        existentes = {a.numero for a in sessao.assentos}
        for numero in range(1, nova_capacidade + 1):
            if numero not in existentes:
                sessao.assentos.append(Assento(numero=numero, ocupado=False))


def atualizar(db: Session, numero: int, dados: SalaUpdate) -> Sala:
    sala = buscar(db, numero)
    if dados.capacidade != sala.capacidade:
        _ajustar_assentos(sala, dados.capacidade)
    sala.capacidade = dados.capacidade
    sala.tipo = dados.tipo
    db.commit()
    db.refresh(sala)
    return sala


def remover(db: Session, numero: int) -> None:
    sala = buscar(db, numero)
    if sala.sessoes:
        raise Conflito(
            f"A sala {numero} tem {len(sala.sessoes)} sessao(oes) vinculada(s). "
            "Remova as sessoes antes de remover a sala."
        )
    db.delete(sala)
    db.commit()
