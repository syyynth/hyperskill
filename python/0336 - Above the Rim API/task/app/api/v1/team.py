from http import HTTPStatus

from flask import Response, jsonify, request
from flask.views import MethodView

from .. import Team, TeamStats, db
from ..team_schema import TeamSchema

team_schema = TeamSchema()


class TeamAPI(MethodView):
    def get(self) -> tuple[Response, HTTPStatus]:
        query = db.select(Team)
        teams = db.session.execute(query).scalars().all()

        return jsonify({'success': True, 'data': {team.short: team.name for team in teams}}), HTTPStatus.OK

    def post(self) -> tuple[Response, HTTPStatus]:
        errors = team_schema.validate(request.json)
        if errors:
            return jsonify({'success': False, 'data': 'Wrong short format'}), HTTPStatus.BAD_REQUEST

        team_short = request.json['short']
        team_name = request.json['name']

        team = Team(short=team_short,
                    name=team_name,
                    stats=TeamStats())

        db.session.add(team)
        db.session.commit()

        return jsonify({'success': True, 'data': 'Team has been added'}), HTTPStatus.CREATED
