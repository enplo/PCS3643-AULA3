class ErroDeDominio(Exception):
    """Erro de regra de negocio, traduzido para HTTP na camada de controller."""

    def __init__(self, mensagem: str):
        self.mensagem = mensagem
        super().__init__(mensagem)


class NaoEncontrado(ErroDeDominio):
    """Recurso inexistente -> 404."""


class Conflito(ErroDeDominio):
    """Choque com o estado atual (duplicata, dependencia) -> 409."""


class RegraViolada(ErroDeDominio):
    """Dados validos isoladamente, mas invalidos no dominio -> 422."""
