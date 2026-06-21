import json
from typing import Dict, Union

from MukeshRobot.modules.no_sql._pg import (
    Session,
    PgCouple,
    PgKarma,
    PgKarmaToggle,
)


async def _get_lovers(chat_id: int) -> dict:
    with Session() as session:
        row = session.query(PgCouple).filter_by(chat_id=chat_id).first()
        if row:
            try:
                return json.loads(row.data)
            except Exception:
                return {}
        return {}


async def get_couple(chat_id: int, date: str):
    lovers = await _get_lovers(chat_id)
    return lovers.get(date, False)


async def save_couple(chat_id: int, date: str, couple: dict):
    lovers = await _get_lovers(chat_id)
    lovers[date] = couple
    with Session() as session:
        row = session.query(PgCouple).filter_by(chat_id=chat_id, date=date).first()
        if row:
            row.data = json.dumps(lovers)
        else:
            session.add(PgCouple(chat_id=chat_id, date=date, data=json.dumps(couple)))
        session.commit()


async def get_karmas_count() -> dict:
    chats_count = 0
    karmas_count = 0
    with Session() as session:
        for row in session.query(PgKarma).filter(PgKarma.chat_id < 0).all():
            if row.karma > 0:
                karmas_count += row.karma
            chats_count += 1
    return {"chats_count": chats_count, "karmas_count": karmas_count}


async def user_global_karma(user_id) -> int:
    total_karma = 0
    key = await int_to_alpha(user_id)
    with Session() as session:
        rows = (
            session.query(PgKarma)
            .filter(PgKarma.chat_id < 0, PgKarma.user_key == key)
            .all()
        )
        for row in rows:
            if row.karma > 0:
                total_karma += row.karma
    return total_karma


async def get_karmas(chat_id: int) -> Dict[str, int]:
    with Session() as session:
        rows = session.query(PgKarma).filter_by(chat_id=chat_id).all()
        return {r.user_key: {"karma": r.karma} for r in rows}


async def get_karma(chat_id: int, name: str) -> Union[bool, dict]:
    name = name.lower().strip()
    karmas = await get_karmas(chat_id)
    return karmas.get(name, None)


async def update_karma(chat_id: int, name: str, karma: dict):
    name = name.lower().strip()
    karma_val = karma.get("karma", 0)
    with Session() as session:
        row = (
            session.query(PgKarma)
            .filter_by(chat_id=chat_id, user_key=name)
            .first()
        )
        if row:
            row.karma = karma_val
        else:
            session.add(PgKarma(chat_id=chat_id, user_key=name, karma=karma_val))
        session.commit()


async def is_karma_on(chat_id: int) -> bool:
    with Session() as session:
        return (
            session.query(PgKarmaToggle).filter_by(chat_id=chat_id).first() is None
        )


async def karma_on(chat_id: int):
    if await is_karma_on(chat_id):
        return
    with Session() as session:
        session.query(PgKarmaToggle).filter_by(chat_id=chat_id).delete()
        session.commit()


async def karma_off(chat_id: int):
    if not await is_karma_on(chat_id):
        return
    with Session() as session:
        session.add(PgKarmaToggle(chat_id=chat_id))
        session.commit()


async def int_to_alpha(user_id: int) -> str:
    alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
    text = ""
    for i in str(user_id):
        text += alphabet[int(i)]
    return text


async def alpha_to_int(user_id_alphabet: str) -> int:
    alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
    user_id = ""
    for i in user_id_alphabet:
        user_id += str(alphabet.index(i))
    return int(user_id)
