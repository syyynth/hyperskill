from http import HTTPStatus

from flask import Response, jsonify, request
from flask.views import MethodView

from .. import Game, Quarters, Team, db


class GameAPI(MethodView):
    def get(self) -> tuple[Response, HTTPStatus]:
        games = db.session.execute(db.select(Game)).scalars().all()
        data = {
            c: self.get_game_score(game)
            for c, game
            in enumerate(games, start=1)
        }

        return jsonify({'success': True, 'data': data}), HTTPStatus.OK

    def post(self, game_id=None) -> tuple[Response, HTTPStatus]:
        payload = request.get_json()
        print(type(payload))

        if game_id is not None:
            response, status = self.update_game(game_id, payload)
        else:
            team_home = self.get_team_by_short(payload.get('home_team'))
            team_visiting = self.get_team_by_short(payload.get('visiting_team'))
            game = Game(home_team=team_home, visiting_team=team_visiting)
            response, status = self.save_game(game)

        return response, status

    def save_game(self, game: Game) -> tuple[Response, HTTPStatus]:
        db.session.add(game)
        db.session.commit()
        return jsonify({'success': True, 'data': game.id}), HTTPStatus.CREATED

    def update_game(self, game_id: str, payload: dict) -> tuple[Response, HTTPStatus]:
        game: Game | None = db.session.execute(db.select(Game).filter_by(id=game_id)).scalar_one_or_none()

        if game is None:
            return jsonify({'success': False, 'data': f'There is no game with id {game_id}'}), HTTPStatus.BAD_REQUEST

        quarter = Quarters(quarters=payload.get('quarters'))
        game.quarters.append(quarter)
        game.home_team_score += int(quarter.quarters.split(':')[0])
        game.visiting_team_score += int(quarter.quarters.split(':')[1])
        db.session.commit()

        return jsonify({'success': True, 'data': 'Score updated'}), HTTPStatus.CREATED

    def get_game_score(self, game: Game) -> str:
        home_team = game.home_team.name
        visiting_team = game.visiting_team.name
        if not game.quarters:
            score = (f'{home_team} {game.home_team_score}:'
                     f'{game.visiting_team_score} {visiting_team}')
        else:
            quarters = ','.join(q.quarters for q in game.quarters)
            score = (f'{home_team} {game.home_team_score}:'
                     f'{game.visiting_team_score} {visiting_team} ({quarters})')
        return score

    def get_team_by_short(self, team_short: str) -> Team:
        return db.session.execute(db.select(Team).filter_by(short=team_short)).scalar_one()
