from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class TipoIngresso(Base):
    __tablename__ = "tipos_ingresso"

    tipo_sala: Mapped[str] = mapped_column(String, primary_key=True)
    valor: Mapped[int] = mapped_column(Integer, nullable=False)
