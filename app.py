import os
from flask import Flask, request, abort, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import db

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_object("config")
    db.init_app(app)
    migrate = Migrate(app, db)
    CORS(app)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
