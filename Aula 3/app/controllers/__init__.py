from app.controllers.filme import router as filmes_router
from app.controllers.sala import router as salas_router
from app.controllers.sessao import router as sessoes_router
from app.controllers.tipo_ingresso import router as tipos_ingresso_router

__all__ = ["filmes_router", "salas_router", "sessoes_router", "tipos_ingresso_router"]
