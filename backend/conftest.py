import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from models import db as _db, DialectWord
from words_blueprint import words_bp
from stats_blueprint import stats_bp
from seed import SEED_DATA


@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    _db.init_app(app)

    app.register_blueprint(words_bp)
    app.register_blueprint(stats_bp)

    with app.app_context():
        _db.create_all()
        for item in SEED_DATA:
            _db.session.add(DialectWord(**item))
        _db.session.commit()

    yield app

    with app.app_context():
        _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
