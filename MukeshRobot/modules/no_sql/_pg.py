import os

from sqlalchemy import create_engine, Column, BigInteger, Integer, Text, UnicodeText
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

_url = os.environ.get("DATABASE_URL", "")
if _url.startswith("postgres://"):
    _url = _url.replace("postgres://", "postgresql://", 1)

engine = create_engine(_url, pool_pre_ping=True, pool_size=5, max_overflow=10)
Session = scoped_session(sessionmaker(bind=engine, autoflush=True, autocommit=False))
Base = declarative_base()


class ServedUser(Base):
    __tablename__ = "served_users"
    user_id = Column(BigInteger, primary_key=True)


class ServedChat(Base):
    __tablename__ = "served_chats"
    chat_id = Column(BigInteger, primary_key=True)


class PgGban(Base):
    __tablename__ = "pg_gban"
    user_id = Column(BigInteger, primary_key=True)
    reason  = Column(UnicodeText, default="None")


class PgAfk(Base):
    __tablename__ = "pg_afk"
    user_id = Column(BigInteger, primary_key=True)
    reason  = Column(UnicodeText, default="")


class PgFsub(Base):
    __tablename__ = "pg_fsub"
    chat_id = Column(BigInteger, primary_key=True)
    channel = Column(UnicodeText, nullable=False, default="")


class PgCouple(Base):
    __tablename__ = "pg_couple"
    chat_id = Column(BigInteger, primary_key=True)
    date    = Column(Text, primary_key=True)
    data    = Column(Text, default="{}")


class PgKarma(Base):
    __tablename__ = "pg_karma"
    chat_id  = Column(BigInteger, primary_key=True)
    user_key = Column(Text, primary_key=True)
    karma    = Column(Integer, default=0)


class PgKarmaToggle(Base):
    __tablename__ = "pg_karma_toggle"
    chat_id = Column(BigInteger, primary_key=True)


Base.metadata.create_all(engine, checkfirst=True)
