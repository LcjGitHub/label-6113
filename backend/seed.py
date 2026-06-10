from models import DialectWord, db

SEED_DATA = [
    {
        "dialect_word": "恰饭",
        "mandarin": "吃饭",
        "region": "江西",
        "example": "你恰饭了冇？",
        "source": "南昌方言调查",
    },
    {
        "dialect_word": "落雨",
        "mandarin": "下雨",
        "region": "广东",
        "example": "今日落雨，唔好出门。",
        "source": "粤语常用词",
    },
    {
        "dialect_word": "晓得",
        "mandarin": "知道",
        "region": "四川",
        "example": "你晓得不晓得这条路？",
        "source": "四川方言词典",
    },
    {
        "dialect_word": "侬",
        "mandarin": "你",
        "region": "上海",
        "example": "侬好，阿拉是上海人。",
        "source": "吴语口语",
    },
    {
        "dialect_word": "忒",
        "mandarin": "太",
        "region": "陕西",
        "example": "这碗面忒香咧！",
        "source": "关中话记录",
    },
]


def seed_database():
    if DialectWord.query.count() > 0:
        return
    for item in SEED_DATA:
        db.session.add(DialectWord(**item))
    db.session.commit()
