from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.controllers import (
    filmes_router,
    salas_router,
    sessoes_router,
    tipos_ingresso_router,
)
from app.database import criar_tabelas
from app.services.erros import Conflito, ErroDeDominio, NaoEncontrado, RegraViolada


@asynccontextmanager
async def lifespan(_app: FastAPI):
    criar_tabelas()
    yield


app = FastAPI(
    title="Cinema API",
    description=(
        "Cadastro de filmes, salas, sessoes e tipos de ingresso de um cinema, "
        "em arquitetura MVC (models / views / controllers + services)."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

STATUS_POR_ERRO = {
    NaoEncontrado: status.HTTP_404_NOT_FOUND,
    Conflito: status.HTTP_409_CONFLICT,
    RegraViolada: status.HTTP_422_UNPROCESSABLE_CONTENT,
}


@app.exception_handler(ErroDeDominio)
async def tratar_erro_de_dominio(_request: Request, erro: ErroDeDominio):
    codigo = STATUS_POR_ERRO.get(type(erro), status.HTTP_400_BAD_REQUEST)
    return JSONResponse(status_code=codigo, content={"detail": erro.mensagem})


app.include_router(filmes_router)
app.include_router(salas_router)
app.include_router(sessoes_router)
app.include_router(tipos_ingresso_router)
