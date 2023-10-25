from datetime import datetime

from flask import request
from sqlalchemy import func, select

import app.models.event as event


class EventService:

    @staticmethod
    def _execute_query(query, session):
        return session.execute(query).scalars().all()

    @classmethod
    def get_events_by_criteria(cls, criteria, session):
        query = select(event.Event).filter(criteria)
        return cls._execute_query(query, session)

    @classmethod
    def get_event_by_id(cls, event_id, session):
        return cls.get_events_by_criteria(event.Event.id == event_id, session)

    @classmethod
    def get_all_events(cls, session):
        return cls._execute_query(select(event.Event), session)

    @classmethod
    def get_events_today(cls, session):
        today_date = datetime.today().date()
        return cls.get_events_by_criteria(func.date(event.Event.date) == today_date, session)

    @classmethod
    def get_events_by_range(cls, session):
        start_time = datetime.strptime(request.args['start_time'], '%Y-%m-%d')
        end_time = datetime.strptime(request.args['end_time'], '%Y-%m-%d')
        return cls.get_events_by_criteria(event.Event.date.between(start_time, end_time), session)
