from MukeshRobot.modules.no_sql._pg import Session, ServedUser


def is_served_user(user_id: int) -> bool:
    with Session() as session:
        return session.query(ServedUser).filter_by(user_id=user_id).first() is not None


def get_served_users() -> list:
    with Session() as session:
        return [{"user_id": u.user_id} for u in session.query(ServedUser).all()]


def save_id(user_id: int):
    if is_served_user(user_id):
        return
    with Session() as session:
        session.add(ServedUser(user_id=user_id))
        session.commit()


def remove_served_users(user_id: int):
    if not is_served_user(user_id):
        return
    with Session() as session:
        session.query(ServedUser).filter_by(user_id=user_id).delete()
        session.commit()
