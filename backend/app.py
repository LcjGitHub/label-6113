import os

from flask import Flask
from flask_cors import CORS

from models import db
from seed import seed_database
from words_blueprint import words_bp
from stats_blueprint import stats_bp

app = Flask(__name__, instance_relative_config=True)

os.makedirs(app.instance_path, exist_ok=True)

db_path = os.path.join(app.instance_path, "dialect.db")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
CORS(app)

app.register_blueprint(words_bp)
app.register_blueprint(stats_bp)


with app.app_context():
    db.create_all()
    with db.engine.connect() as conn:
        columns = [row[1] for row in conn.execute(db.text("PRAGMA table_info(dialect_words)"))]
        if "remark" not in columns:
            conn.execute(db.text("ALTER TABLE dialect_words ADD COLUMN remark TEXT DEFAULT ''"))
            conn.commit()
        if "pinyin" not in columns:
            conn.execute(db.text("ALTER TABLE dialect_words ADD COLUMN pinyin VARCHAR(200) DEFAULT ''"))
            conn.commit()
    seed_database()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000, debug=True)
