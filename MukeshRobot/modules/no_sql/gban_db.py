from MukeshRobot.modules.no_sql._pg import Session, PgGban


def is_user_ingbanned(user_id: int) -> bool:
    with Session() as session:
        return session.query(PgGban).filter_by(user_id=user_id).first() is not None


def add_gban(user_id: int, gban_reason: str = None):
    if is_user_ingbanned(user_id):
        return
    with Session() as session:
        session.add(PgGban(user_id=user_id, reason=gban_reason or "None"))
        session.commit()


def remove_gban(user_id: int):
    if not is_user_ingbanned(user_id):
        return
    with Session() as session:
        session.query(PgGban).filter_by(user_id=user_id).delete()
        session.commit()


def is_gban(user_id: int) -> bool:
    with Session() as session:
        return (
            session.query(PgGban)
            .filter(PgGban.user_id == user_id, PgGban.reason != "None")
            .first()
            is not None
        )


def get_gban_list() -> list:
    with Session() as session:
        return [
            {"user_id": g.user_id, "gban_reason": g.reason}
            for g in session.query(PgGban).filter(PgGban.reason != "None").all()
        ]
