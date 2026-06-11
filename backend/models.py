from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class DialectWord(db.Model):
    __tablename__ = "dialect_words"

    id = db.Column(db.Integer, primary_key=True)
    dialect_word = db.Column(db.String(100), nullable=False)
    mandarin = db.Column(db.String(100), nullable=False)
    pinyin = db.Column(db.String(200), default="")
    region = db.Column(db.String(50), nullable=False)
    example = db.Column(db.Text, default="")
    source = db.Column(db.String(200), default="")
    remark = db.Column(db.Text, default="")

    def to_dict(self):
        return {
            "id": self.id,
            "dialect_word": self.dialect_word,
            "mandarin": self.mandarin,
            "pinyin": self.pinyin or "",
            "region": self.region,
            "example": self.example or "",
            "source": self.source or "",
            "remark": self.remark or "",
        }
