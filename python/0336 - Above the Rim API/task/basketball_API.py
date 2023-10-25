import sys
from http import HTTPStatus

from flask import Response, jsonify, render_template

from app import create_app, db

app = create_app()


@app.route('/')
def main() -> tuple[str, HTTPStatus]:
    return render_template('index.html'), HTTPStatus.OK


@app.errorhandler(404)
def not_found(_) -> tuple[Response, HTTPStatus]:
    return jsonify({'success': False, 'data': 'Wrong address'}), HTTPStatus.NOT_FOUND


if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()

    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=int(arg_port))
    else:
        app.run(debug=True)
