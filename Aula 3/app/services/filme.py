from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Filme
from app.services.erros import Conflito, NaoEncontrado
from app.views.filme import FilmeCreate, FilmeUpdate


def listar(db: Session) -> list[Filme]:
    return list(db.scalars(select(Filme).order_by(Filme.codigo)))


def buscar(db: Session, codigo: int) -> Filme:
    filme = db.get(Filme, codigo)
    if filme is None:
        raise NaoEncontrado(f"Filme de codigo {codigo} nao encontrado.")
    return filme


def _garantir_nome_livre(db: Session, nome: str, ignorar: int | None = None) -> None:
    consulta = select(Filme).where(func.lower(Filme.nome) == nome.lower())
    if ignorar is not None:
        consulta = consulta.where(Filme.codigo != ignorar)
    if db.scalar(consulta) is not None:
        raise Conflito(f"Ja existe um filme cadastrado com o nome '{nome}'.")


def criar(db: Session, dados: FilmeCreate) -> Filme:
    _garantir_nome_livre(db, dados.nome)
    filme = Filme(**dados.model_dump())
    db.add(filme)
    db.commit()
    db.refresh(filme)
    return filme


def atualizar(db: Session, codigo: int, dados: FilmeUpdate) -> Filme:
    filme = buscar(db, codigo)
    _garantir_nome_livre(db, dados.nome, ignorar=codigo)
    for campo, valor in dados.model_dump().items():
        setattr(filme, campo, valor)
    db.commit()
    db.refresh(filme)
    return filme


def remover(db: Session, codigo: int) -> None:
    filme = buscar(db, codigo)
    if filme.sessoes:
        raise Conflito(
            f"O filme {codigo} tem {len(filme.sessoes)} sessao(oes) vinculada(s). "
            "Remova as sessoes antes de remover o filme."
        )
    db.delete(filme)
    db.commit()
