from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import db


class Quarters(db.Model):
    __tablename__ = 'quarters'

    id: Mapped[int] = mapped_column(primary_key=True)
    game_id: Mapped[int] = mapped_column(ForeignKey('games.id'))
    quarters: Mapped[str] = mapped_column(String(50))
