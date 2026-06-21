from MukeshRobot.modules.no_sql._pg import Session, PgFsub


def fs_settings(chat_id: int):
    with Session() as session:
        fsub = session.query(PgFsub).filter_by(chat_id=chat_id).first()
        if fsub:
            return {"chat_id": fsub.chat_id, "channel": fsub.channel}
        return None


def add_channel(chat_id: int, channel):
    with Session() as session:
        fsub = session.query(PgFsub).filter_by(chat_id=chat_id).first()
        if fsub:
            fsub.channel = str(channel)
        else:
            session.add(PgFsub(chat_id=chat_id, channel=str(channel)))
        session.commit()


def disapprove(chat_id: int):
    with Session() as session:
        session.query(PgFsub).filter_by(chat_id=chat_id).delete()
        session.commit()
