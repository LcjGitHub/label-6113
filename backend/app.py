import os

from flask import Flask, jsonify, request
from flask_cors import CORS

from models import DialectWord, db
from seed import seed_database

app = Flask(__name__, instance_relative_config=True)

os.makedirs(app.instance_path, exist_ok=True)

db_path = os.path.join(app.instance_path, "dialect.db")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
CORS(app)


@app.route("/api/words", methods=["GET"])
def list_words():
    region = request.args.get("region", "").strip()
    query = DialectWord.query
    if region:
        query = query.filter(DialectWord.region == region)
    words = query.order_by(DialectWord.id).all()
    return jsonify([word.to_dict() for word in words])


@app.route("/api/words/<int:word_id>", methods=["GET"])
def get_word(word_id):
    word = db.session.get(DialectWord, word_id)
    if not word:
        return jsonify({"error": "词条不存在"}), 404
    return jsonify(word.to_dict())


@app.route("/api/words", methods=["POST"])
def create_word():
    data = request.get_json(silent=True) or {}
    error = _validate_word_data(data)
    if error:
        return jsonify({"error": error}), 400

    word = DialectWord(
        dialect_word=data["dialect_word"].strip(),
        mandarin=data["mandarin"].strip(),
        region=data["region"].strip(),
        example=(data.get("example") or "").strip(),
        source=(data.get("source") or "").strip(),
    )
    db.session.add(word)
    db.session.commit()
    return jsonify(word.to_dict()), 201


@app.route("/api/words/<int:word_id>", methods=["PUT"])
def update_word(word_id):
    word = db.session.get(DialectWord, word_id)
    if not word:
        return jsonify({"error": "词条不存在"}), 404

    data = request.get_json(silent=True) or {}
    error = _validate_word_data(data)
    if error:
        return jsonify({"error": error}), 400

    word.dialect_word = data["dialect_word"].strip()
    word.mandarin = data["mandarin"].strip()
    word.region = data["region"].strip()
    word.example = (data.get("example") or "").strip()
    word.source = (data.get("source") or "").strip()
    db.session.commit()
    return jsonify(word.to_dict())


@app.route("/api/words/<int:word_id>", methods=["DELETE"])
def delete_word(word_id):
    word = db.session.get(DialectWord, word_id)
    if not word:
        return jsonify({"error": "词条不存在"}), 404
    db.session.delete(word)
    db.session.commit()
    return jsonify({"message": "删除成功"})


@app.route("/api/regions", methods=["GET"])
def list_regions():
    rows = db.session.query(DialectWord.region).distinct().order_by(DialectWord.region).all()
    return jsonify([row[0] for row in rows])


def _validate_word_data(data):
    required = ("dialect_word", "mandarin", "region")
    for field in required:
        value = (data.get(field) or "").strip()
        if not value:
            labels = {
                "dialect_word": "方言词",
                "mandarin": "普通话",
                "region": "地区",
            }
            return f"{labels[field]}不能为空"
    return None


with app.app_context():
    db.create_all()
    seed_database()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000, debug=True)
