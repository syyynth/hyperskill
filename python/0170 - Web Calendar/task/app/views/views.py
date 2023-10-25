from http import HTTPStatus

from flask import Response, jsonify, request
from flask.views import MethodView
from marshmallow import ValidationError

import app.dao.dao as dao
import app.database as database
import app.models.event as event_model
import app.schemas.schemas as event_schemas

event_schema = event_schemas.EventSchema()


class EventAPI(MethodView):
    """
    This class implements the endpoints for retrieving, adding, and deleting events.

    Methods:
        get: Retrieves events by ID or range or 'today'.
        post: Adds a new event.
        delete: Deletes an event by ID.
    """

    def get(self, event_id: int | None = None) -> tuple[Response, HTTPStatus]:
        """
        Get event(s) by ID, by ID = 'today', by passing arguments
        (e.g. ?start_time=XXXX-XX-XX&end_time=XXXX-XX-XX). If None, returns all events.

        :param event_id: The event ID or 'today' for today's events.
        :return: A tuple containing the response and HTTP status.
        """
        with database.Session() as session:
            events, is_single = self._retrieve_events(session, event_id)
            response = self._format_response(all_events=events, is_single=is_single)

        return response

    def _retrieve_events(self, session, event_id) -> tuple[list, bool]:
        is_single = False

        if request.args:
            events = dao.EventService.get_events_by_range(session)
        elif event_id == 'today':
            events = dao.EventService.get_events_today(session)
        elif event_id is None:
            events = dao.EventService.get_all_events(session)
        else:
            events = dao.EventService.get_event_by_id(event_id, session)
            is_single = True

        return events, is_single

    def _format_response(self, all_events: list, is_single: bool) -> tuple[Response, HTTPStatus]:
        if not all_events:
            return jsonify({'message': "The event doesn't exist!"}), HTTPStatus.NOT_FOUND

        response = [event.to_dict() for event in all_events]

        if not is_single:
            return jsonify(response), HTTPStatus.OK

        return jsonify(response[0]), HTTPStatus.OK

    def post(self) -> tuple[Response, HTTPStatus]:
        """
        Process a POST request to create a new event.

        :return: A tuple containing a Flask Response object and the HTTP status code.
        """
        try:
            event_data = event_schema.load(request.form)
            response = self._save_event(event_data)
        except ValidationError as err:
            message = {key: value[0] for key, value in err.messages.items()}
            return jsonify({'message': message}), HTTPStatus.BAD_REQUEST

        return response

    def _save_event(self, event_data) -> tuple[Response, HTTPStatus]:
        event = event_model.Event(**event_data)

        with database.Session.begin() as session:
            session.add(event)

        return jsonify({'message': 'The event has been added!',
                        'event': event_data['event'],
                        'date': event_data['date'].isoformat()}), HTTPStatus.OK

    def delete(self, event_id=None) -> tuple[Response, HTTPStatus]:
        """
        Delete an event.

        :param event_id: The ID of the event to delete.
        :return: A tuple containing a JSON response and an HTTP status code.
        """
        with database.Session.begin() as session:
            selected_event = dao.EventService.get_event_by_id(event_id, session)

            if not selected_event:
                return jsonify({'message': "The event doesn't exist!"}), HTTPStatus.NOT_FOUND

            session.delete(selected_event[0])

        return jsonify({'message': 'The event has been deleted!'}), HTTPStatus.OK
