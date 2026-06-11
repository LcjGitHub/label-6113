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


@app.route("/api/words/search", methods=["GET"])
def search_words():
    keyword = request.args.get("keyword", "").strip()
    region = request.args.get("region", "").strip()
    if not keyword:
        return jsonify({"error": "关键词不能为空"}), 400
    query = DialectWord.query
    like_pattern = f"%{keyword}%"
    query = query.filter(
        db.or_(
            DialectWord.dialect_word.like(like_pattern),
            DialectWord.mandarin.like(like_pattern),
        )
    )
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
        remark=(data.get("remark") or "").strip(),
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
    word.remark = (data.get("remark") or "").strip()
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


@app.route("/api/words/random", methods=["GET"])
def get_random_word():
    word = DialectWord.query.order_by(db.func.random()).first()
    if not word:
        return jsonify({"error": "暂无词条数据"}), 404
    return jsonify(word.to_dict())


@app.route("/api/regions", methods=["GET"])
def list_regions():
    rows = db.session.query(DialectWord.region).distinct().order_by(DialectWord.region).all()
    return jsonify([row[0] for row in rows])


@app.route("/api/stats/region", methods=["GET"])
def region_stats():
    stats = (
        db.session.query(
            DialectWord.region,
            db.func.count(DialectWord.id).label("count"),
        )
        .group_by(DialectWord.region)
        .order_by(db.desc("count"))
        .all()
    )
    total = db.session.query(db.func.count(DialectWord.id)).scalar() or 0
    return jsonify(
        {
            "total": total,
            "regions": [
                {"region": row.region, "count": row.count} for row in stats
            ],
        }
    )


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
    with db.engine.connect() as conn:
        columns = [row[1] for row in conn.execute(db.text("PRAGMA table_info(dialect_words)"))]
        if "remark" not in columns:
            conn.execute(db.text("ALTER TABLE dialect_words ADD COLUMN remark TEXT DEFAULT ''"))
            conn.commit()
    seed_database()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000, debug=True)
