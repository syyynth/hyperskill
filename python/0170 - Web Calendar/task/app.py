import sys

from flask import Flask

import app.database as db
import app.views.views as views

if __name__ == '__main__':
    app = Flask(__name__)

    event_view = views.EventAPI.as_view('event_api')
    app.add_url_rule('/event', view_func=event_view, methods=['GET', 'POST'])
    app.add_url_rule('/event/<event_id>', view_func=event_view, methods=['GET', 'DELETE'])

    db.Base.metadata.drop_all(db.engine)
    db.Base.metadata.create_all(db.engine)

    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run(host='0.0.0.0', debug=True)
