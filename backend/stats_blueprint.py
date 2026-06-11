from flask import Blueprint, jsonify

from models import DialectWord, db

stats_bp = Blueprint("stats", __name__, url_prefix="/api")


@stats_bp.route("/regions", methods=["GET"])
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


@stats_bp.route("/stats/region", methods=["GET"])
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
