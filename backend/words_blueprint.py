from flask import Blueprint, jsonify, request

from models import DialectWord, db

words_bp = Blueprint("words", __name__, url_prefix="/api/words")


@words_bp.route("", methods=["GET"])
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
                DialectWord.pinyin.like(like_pattern),
            )
        )
    words = query.order_by(DialectWord.id).all()
    return jsonify([word.to_dict() for word in words])


@words_bp.route("/<int:word_id>", methods=["GET"])
def get_word(word_id):
    word = db.session.get(DialectWord, word_id)
    if not word:
        return jsonify({"error": "词条不存在"}), 404
    return jsonify(word.to_dict())


@words_bp.route("", methods=["POST"])
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


@words_bp.route("/<int:word_id>", methods=["PUT"])
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


@words_bp.route("/<int:word_id>", methods=["DELETE"])
def delete_word(word_id):
    word = db.session.get(DialectWord, word_id)
    if not word:
        return jsonify({"error": "词条不存在"}), 404
    db.session.delete(word)
    db.session.commit()
    return jsonify({"message": "删除成功"})


@words_bp.route("/batch-delete", methods=["POST"])
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


@words_bp.route("/random", methods=["GET"])
def get_random_word():
    region = request.args.get("region", "").strip()
    query = DialectWord.query
    if region:
        query = query.filter(DialectWord.region == region)
    word = query.order_by(db.func.random()).first()
    if not word:
        return jsonify({"error": "暂无词条数据"}), 404
    return jsonify(word.to_dict())


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
