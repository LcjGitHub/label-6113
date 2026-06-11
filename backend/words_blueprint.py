import csv
import io

from flask import Blueprint, jsonify, request, make_response

from models import DialectWord, db

words_bp = Blueprint("words", __name__, url_prefix="/api/words")


SORT_FIELD_MAP = {
    "id": DialectWord.id,
    "dialect_word": DialectWord.dialect_word,
    "region": DialectWord.region,
}


@words_bp.route("", methods=["GET"])
def list_words():
    region = request.args.get("region", "").strip()
    keyword = request.args.get("keyword", "").strip()
    tag = request.args.get("tag", "").strip()
    sort_field = request.args.get("sort_field", "id").strip()
    sort_direction = request.args.get("sort_direction", "asc").strip()
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
    if tag:
        query = query.filter(db.literal(",").concat(DialectWord.tags).concat(",").like(f"%,{tag},%"))
    column = SORT_FIELD_MAP.get(sort_field, DialectWord.id)
    order_col = column.desc() if sort_direction == "desc" else column.asc()
    words = query.order_by(order_col).all()
    return jsonify([word.to_dict() for word in words])


@words_bp.route("/export", methods=["GET"])
def export_words():
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

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["方言词", "普通话", "拼音", "地区", "例句", "来源", "备注", "标签"])
    for word in words:
        writer.writerow([
            word.dialect_word or "",
            word.mandarin or "",
            word.pinyin or "",
            word.region or "",
            word.example or "",
            word.source or "",
            word.remark or "",
            word.tags or "",
        ])

    output.seek(0)
    response = make_response(output.getvalue())
    response.headers["Content-Type"] = "text/csv; charset=utf-8"
    response.headers["Content-Disposition"] = "attachment; filename=dialect_words.csv"
    return response


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
        tags=(data.get("tags") or "").strip(),
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
    word.tags = (data.get("tags") or "").strip()
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


@words_bp.route("/batch-import", methods=["POST"])
def batch_import_words():
    data = request.get_json(silent=True) or {}
    items = data.get("items", [])
    if not isinstance(items, list) or len(items) == 0:
        return jsonify({"error": "请提供词条对象数组"}), 400

    success_count = 0
    fail_count = 0
    failed_items = []

    for index, item in enumerate(items):
        if not isinstance(item, dict):
            fail_count += 1
            failed_items.append({"index": index, "error": "数据格式错误，不是有效的对象"})
            continue

        error = _validate_word_data(item)
        if error:
            fail_count += 1
            failed_items.append({"index": index, "error": error})
            continue

        try:
            word = DialectWord(
                dialect_word=item["dialect_word"].strip(),
                mandarin=item["mandarin"].strip(),
                pinyin=(item.get("pinyin") or "").strip(),
                region=item["region"].strip(),
                example=(item.get("example") or "").strip(),
                source=(item.get("source") or "").strip(),
                remark=(item.get("remark") or "").strip(),
                tags=(item.get("tags") or "").strip(),
            )
            db.session.add(word)
            success_count += 1
        except Exception as e:
            fail_count += 1
            failed_items.append({"index": index, "error": f"添加失败: {str(e)}"})

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"保存数据时发生错误: {str(e)}"}), 500

    return jsonify({
        "success_count": success_count,
        "fail_count": fail_count,
        "failed_items": failed_items,
    })


@words_bp.route("/<int:word_id>/adjacent", methods=["GET"])
def get_adjacent_words(word_id):
    word = db.session.get(DialectWord, word_id)
    if not word:
        return jsonify({"error": "词条不存在"}), 404

    prev_word = (
        DialectWord.query
        .filter(DialectWord.id < word_id)
        .order_by(DialectWord.id.desc())
        .first()
    )
    next_word = (
        DialectWord.query
        .filter(DialectWord.id > word_id)
        .order_by(DialectWord.id.asc())
        .first()
    )

    return jsonify({
        "prev": {
            "id": prev_word.id,
            "dialect_word": prev_word.dialect_word,
        } if prev_word else None,
        "next": {
            "id": next_word.id,
            "dialect_word": next_word.dialect_word,
        } if next_word else None,
    })


@words_bp.route("/tags", methods=["GET"])
def list_tags():
    words = DialectWord.query.order_by(DialectWord.id).all()
    tag_set = set()
    for word in words:
        if word.tags:
            for t in word.tags.split(","):
                t = t.strip()
                if t:
                    tag_set.add(t)
    return jsonify(sorted(tag_set))


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
