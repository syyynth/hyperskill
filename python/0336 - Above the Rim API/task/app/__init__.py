from flask import Flask

from .api.v1.game import GameAPI as Game_API_V1
from .api.v1.team import TeamAPI
from .api.v1.team_info import TeamInfoAPI
from .api.v2.game import GameAPI as Game_API_V2
from .config import Config
from .models import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    app.add_url_rule('/api/v1/teams', view_func=TeamAPI.as_view('v1_teams'))
    app.add_url_rule('/api/v1/team/<short>', view_func=TeamInfoAPI.as_view('v1_team_short'))
    app.add_url_rule('/api/v1/games', view_func=Game_API_V1.as_view('v1_games'))
    app.add_url_rule('/api/v2/games', view_func=Game_API_V2.as_view('v2_games'))
    app.add_url_rule('/api/v2/games/<game_id>', view_func=Game_API_V2.as_view('v2_games_game_id'))

    return app
