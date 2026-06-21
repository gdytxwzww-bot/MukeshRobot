from MukeshRobot.modules.no_sql._pg import Session, ServedChat


def get_served_chats() -> list:
    with Session() as session:
        return [{"chat_id": c.chat_id} for c in session.query(ServedChat).all()]


def is_served_chat(chat_id: int) -> bool:
    with Session() as session:
        return session.query(ServedChat).filter_by(chat_id=chat_id).first() is not None


def add_served_chat(chat_id: int):
    if is_served_chat(chat_id):
        return
    with Session() as session:
        session.add(ServedChat(chat_id=chat_id))
        session.commit()


def remove_served_chat(chat_id: int):
    if not is_served_chat(chat_id):
        return
    with Session() as session:
        session.query(ServedChat).filter_by(chat_id=chat_id).delete()
        session.commit()
