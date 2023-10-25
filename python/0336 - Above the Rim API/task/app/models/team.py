from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import db


class Team(db.Model):
    __tablename__ = 'teams'

    id: Mapped[int] = mapped_column(primary_key=True)
    short: Mapped[str] = mapped_column(String(3), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    stats: Mapped['TeamStats'] = relationship(backref='team', uselist=False)

    def info(self) -> dict:
        return {
            'short': self.short,
            'name': self.name,
            'win': self.stats.win,
            'lost': self.stats.lost
        }
