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
    keyword = request.args.get("keyword", "").strip()
    query = DialectWord.query
    if region:
        query = query.filter(DialectWord.region == region)
    if keyword:
        like_pattern = f"%{keyword}%"
        query = query.filter(
            db.or_(
                DialectWord.dialect_word.like(like_pattern),
                DialectWord.mandarin.like(like_pattern),
            )
        )
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
        pinyin=(data.get("pinyin") or "").strip(),
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
    word.pinyin = (data.get("pinyin") or "").strip()
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


@app.route("/api/words/batch-delete", methods=["POST"])
def batch_delete_words():
    data = request.get_json(silent=True) or {}
    ids = data.get("ids", [])
    if not isinstance(ids, list) or len(ids) == 0:
        return jsonify({"error": "请提供要删除的词条编号数组"}), 400

    valid_ids = []
    for wid in ids:
        if isinstance(wid, int) and wid > 0:
            valid_ids.append(wid)
        elif isinstance(wid, str) and wid.isdigit():
            valid_ids.append(int(wid))

    if not valid_ids:
        return jsonify({"error": "无效的词条编号"}), 400

    words_to_delete = DialectWord.query.filter(DialectWord.id.in_(valid_ids)).all()
    deleted_count = len(words_to_delete)
    for word in words_to_delete:
        db.session.delete(word)
    db.session.commit()
    return jsonify({"deleted_count": deleted_count})


@app.route("/api/words/random", methods=["GET"])
def get_random_word():
    word = DialectWord.query.order_by(db.func.random()).first()
    if not word:
        return jsonify({"error": "暂无词条数据"}), 404
    return jsonify(word.to_dict())


@app.route("/api/regions", methods=["GET"])
def list_regions():
    rows = (
        db.session.query(
            DialectWord.region,
            db.func.count(DialectWord.id).label("count"),
        )
        .group_by(DialectWord.region)
        .order_by(DialectWord.region)
        .all()
    )
    return jsonify([{"region": row.region, "count": row.count} for row in rows])


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
        if "pinyin" not in columns:
            conn.execute(db.text("ALTER TABLE dialect_words ADD COLUMN pinyin VARCHAR(200) DEFAULT ''"))
            conn.commit()
    seed_database()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000, debug=True)
