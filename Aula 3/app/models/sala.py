from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Sala(Base):
    __tablename__ = "salas"

    numero: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    capacidade: Mapped[int] = mapped_column(Integer, nullable=False)
    tipo: Mapped[str] = mapped_column(String, nullable=False)

    sessoes: Mapped[list["Sessao"]] = relationship(back_populates="sala")  # noqa: F821
