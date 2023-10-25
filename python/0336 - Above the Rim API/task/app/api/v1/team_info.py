from http import HTTPStatus

from flask import Response, jsonify
from flask.views import MethodView

from .. import Team, db


class TeamInfoAPI(MethodView):
    def get(self, short) -> tuple[Response, HTTPStatus]:
        query = db.select(Team).where(Team.short == short)
        team = db.session.execute(query).scalar_one_or_none()

        if not team:
            return jsonify({'success': False, 'data': f'There is no team {short}'}), HTTPStatus.BAD_REQUEST

        return jsonify({'success': True, 'data': team.info()}), HTTPStatus.OK
