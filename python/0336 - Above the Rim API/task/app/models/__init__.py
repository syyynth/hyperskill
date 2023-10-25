from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .game import Game
from .team import Team
from .team_stats import TeamStats
from .quarters import Quarters
