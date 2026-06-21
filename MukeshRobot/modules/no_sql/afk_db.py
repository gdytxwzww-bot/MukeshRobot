from MukeshRobot.modules.no_sql._pg import Session, PgAfk


async def is_afk(user_id: int):
    with Session() as session:
        user = session.query(PgAfk).filter_by(user_id=user_id).first()
        if not user:
            return False, {}
        return True, user.reason


async def add_afk(user_id: int, mode):
    with Session() as session:
        user = session.query(PgAfk).filter_by(user_id=user_id).first()
        if user:
            user.reason = mode
        else:
            session.add(PgAfk(user_id=user_id, reason=mode))
        session.commit()


async def remove_afk(user_id: int):
    with Session() as session:
        session.query(PgAfk).filter_by(user_id=user_id).delete()
        session.commit()


async def get_afk_users() -> list:
    with Session() as session:
        return [
            {"user_id": u.user_id, "reason": u.reason}
            for u in session.query(PgAfk).all()
        ]
