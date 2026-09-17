from datetime import date

from sqlalchemy import Date, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Filme(Base):
    __tablename__ = "filmes"

    codigo: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    data_estreia: Mapped[date] = mapped_column(Date, nullable=False)
    data_saida: Mapped[date] = mapped_column(Date, nullable=False)
    duracao: Mapped[int] = mapped_column(Integer, nullable=False)

    sessoes: Mapped[list["Sessao"]] = relationship(back_populates="filme")
