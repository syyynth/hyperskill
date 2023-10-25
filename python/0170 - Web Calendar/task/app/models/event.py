from datetime import datetime

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

import app.database as db


class Event(db.Base):
    """Event model class"""
    __tablename__ = 'events'
    id: Mapped[int] = mapped_column(primary_key=True)
    event: Mapped[str] = mapped_column(String(80), nullable=False)
    date: Mapped[datetime] = mapped_column(nullable=False)

    def to_dict(self):
        """Represents instance data as a dictionary"""
        return dict(id=self.id,
                    event=self.event,
                    date=self.date.strftime('%Y-%m-%d'))
