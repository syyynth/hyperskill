import sys

from flask import Flask

import models
import recipe_api

if __name__ == '__main__':
    app = Flask(__name__)

    models.Base.metadata.drop_all(models.engine)
    models.Base.metadata.create_all(models.engine)

    urls = [
        ('/api/recipe', None, ['GET']),
        ('/api/recipe/<int:recipe_id>', None, ['GET', 'DELETE', 'PUT']),
        ('/api/recipe/new', None, ['POST']),
    ]

    recipe_view = recipe_api.RecipeAPI.as_view('recipe_api')

    for url, defaults, methods in urls:
        app.add_url_rule(url,
                         defaults=defaults,
                         view_func=recipe_view,
                         methods=methods)

    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run(host='0.0.0.0', port=5000, debug=True)
