from http import HTTPStatus

from flask import Response, jsonify, request
from flask.views import MethodView
from sqlalchemy.orm.exc import NoResultFound

from .. import Game, Team, db


class GameAPI(MethodView):
    def get(self) -> tuple[Response, HTTPStatus]:
        games = db.session.execute(db.select(Game)).scalars().all()

        scores = self._formatted_scores(games)
        return jsonify({'success': True, 'data': scores}), HTTPStatus.OK

    def post(self) -> tuple[Response, HTTPStatus]:
        payload = request.get_json()

        try:
            home_team, visiting_team, home_team_score, visiting_team_score = self._process_payload(payload)
        except NoResultFound:
            return jsonify({'success': False, 'data': 'Wrong team short'}), HTTPStatus.BAD_REQUEST

        game = self._make_game(home_team, visiting_team, home_team_score, visiting_team_score)

        try:
            self._add_game(game)
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'data': str(e)}), HTTPStatus.BAD_REQUEST

        return jsonify({'success': True, 'data': 'Game has been added'}), HTTPStatus.CREATED

    def _formatted_scores(self, games):
        return {
            count: (f'{game.home_team.name} {game.home_team_score}:'
                    f'{game.visiting_team_score} {game.visiting_team.name}')
            for count, game in enumerate(games, start=1)}

    def _process_payload(self, payload):
        home_team = self._get_team(payload.get('home_team'))
        visiting_team = self._get_team(payload.get('visiting_team'))
        home_team_score = payload['home_team_score']
        visiting_team_score = payload['visiting_team_score']
        return home_team, visiting_team, home_team_score, visiting_team_score

    def _get_team(self, team_short):
        return db.session.execute(db.select(Team).filter_by(short=team_short)).scalar_one()

    def _make_game(self, home_team, visiting_team, home_team_score, visiting_team_score):
        return Game(home_team=home_team,
                    visiting_team=visiting_team,
                    home_team_score=home_team_score,
                    visiting_team_score=visiting_team_score)

    def _add_game(self, game):
        db.session.add(game)
        self._update_stats(game)
        db.session.commit()

    def _update_stats(self, game):
        home_team = game.home_team
        visiting_team = game.visiting_team
        home_team_score = game.home_team_score
        visiting_team_score = game.visiting_team_score

        if home_team_score > visiting_team_score:
            home_team.stats.win += 1
            visiting_team.stats.lost += 1
        elif home_team_score < visiting_team_score:
            home_team.stats.lost += 1
            visiting_team.stats.win += 1
