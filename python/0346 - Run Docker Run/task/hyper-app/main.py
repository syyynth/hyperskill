"""
Do not change this file!
"""

from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/')
def home():
    return jsonify(
        {
            "id": "90",
            "first_name": "Hyper",
            "last_name": "Skill",
        }
    )


if __name__ == '__main__':
    print("This is hyper-app!")
    app.run(host="0.0.0.0", port=8000)
