from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from . import db


class TeamStats(db.Model):
    __tablename__ = 'team_stats'

    team_id: Mapped[int] = mapped_column(ForeignKey('teams.id'), primary_key=True)
    win: Mapped[int] = mapped_column(default=0)
    lost: Mapped[int] = mapped_column(default=0)
