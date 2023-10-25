from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import db


class Game(db.Model):
    __tablename__ = 'games'

    id: Mapped[int] = mapped_column(primary_key=True)
    home_team_id: Mapped[int] = mapped_column(ForeignKey('teams.id'))
    visiting_team_id: Mapped[int] = mapped_column(ForeignKey('teams.id'))
    home_team_score: Mapped[int] = mapped_column(default=0)
    visiting_team_score: Mapped[int] = mapped_column(default=0)

    home_team: Mapped['Team'] = relationship(foreign_keys=[home_team_id])
    visiting_team: Mapped['Team'] = relationship(foreign_keys=[visiting_team_id])

    quarters: Mapped[list['Quarters']] = relationship()
