from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.services import filme as servico
from app.views.filme import FilmeCreate, FilmeOut, FilmeUpdate

router = APIRouter(prefix="/filmes", tags=["Filmes"])


@router.get("", response_model=list[FilmeOut], summary="Lista todos os filmes")
def listar(db: Session = Depends(get_db)):
    return servico.listar(db)


@router.get("/{codigo}", response_model=FilmeOut, summary="Detalha um filme")
def buscar(codigo: int, db: Session = Depends(get_db)):
    return servico.buscar(db, codigo)


@router.post("", response_model=FilmeOut, status_code=status.HTTP_201_CREATED,
             summary="Cadastra um filme")
def criar(dados: FilmeCreate, db: Session = Depends(get_db)):
    return servico.criar(db, dados)


@router.put("/{codigo}", response_model=FilmeOut, summary="Edita um filme")
def atualizar(codigo: int, dados: FilmeUpdate, db: Session = Depends(get_db)):
    return servico.atualizar(db, codigo, dados)


@router.delete("/{codigo}", status_code=status.HTTP_204_NO_CONTENT,
               summary="Remove um filme")
def remover(codigo: int, db: Session = Depends(get_db)):
    servico.remover(db, codigo)
