from datetime import date

from sqlalchemy import Boolean, Date, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Sessao(Base):
    __tablename__ = "sessoes"
    __table_args__ = (
        UniqueConstraint("sala_numero", "data", "hora_inicio", name="uq_sessao_sala_data_hora"),
    )

    codigo: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sala_numero: Mapped[int] = mapped_column(ForeignKey("salas.numero"), nullable=False)
    filme_codigo: Mapped[int] = mapped_column(ForeignKey("filmes.codigo"), nullable=False)
    data: Mapped[date] = mapped_column(Date, nullable=False)
    hora_inicio: Mapped[int] = mapped_column(Integer, nullable=False)

    sala: Mapped["Sala"] = relationship(back_populates="sessoes")
    filme: Mapped["Filme"] = relationship(back_populates="sessoes")
    assentos: Mapped[list["Assento"]] = relationship(
        back_populates="sessao",
        cascade="all, delete-orphan",
        order_by="Assento.numero",
    )

    @property
    def capacidade(self) -> int:
        return len(self.assentos)

    @property
    def assentos_livres(self) -> int:
        return sum(1 for assento in self.assentos if not assento.ocupado)

    @property
    def tem_ingresso_vendido(self) -> bool:
        return any(assento.ocupado for assento in self.assentos)


class Assento(Base):
    __tablename__ = "assentos"
    __table_args__ = (
        UniqueConstraint("sessao_codigo", "numero", name="uq_assento_sessao_numero"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sessao_codigo: Mapped[int] = mapped_column(ForeignKey("sessoes.codigo"), nullable=False)
    numero: Mapped[int] = mapped_column(Integer, nullable=False)
    ocupado: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    sessao: Mapped["Sessao"] = relationship(back_populates="assentos")
