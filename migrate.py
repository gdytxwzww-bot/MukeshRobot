#!/usr/bin/env python3
"""
migrate.py — MukeshRobot PostgreSQL Migration Verifier
=======================================================
Verifies that all required PostgreSQL tables exist and are reachable.
Safe to run multiple times (idempotent — creates tables only if absent).

Usage (Railway console or locally):
    python3 migrate.py

Exit codes:
    0  — all tables present and healthy
    1  — connection failed or a table is missing
"""

import os
import sys

# ── Colour helpers ──────────────────────────────────────────────────────────
GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
RESET  = "\033[0m"
BOLD   = "\033[1m"

def ok(msg):   print(f"  {GREEN}✔{RESET}  {msg}")
def fail(msg): print(f"  {RED}✖{RESET}  {msg}")
def info(msg): print(f"  {CYAN}→{RESET}  {msg}")
def warn(msg): print(f"  {YELLOW}⚠{RESET}  {msg}")

# ── 1. Read DATABASE_URL ────────────────────────────────────────────────────
print(f"\n{BOLD}{'─'*55}{RESET}")
print(f"{BOLD}  MukeshRobot — PostgreSQL Migration Verifier{RESET}")
print(f"{BOLD}{'─'*55}{RESET}\n")

DATABASE_URL = os.environ.get("DATABASE_URL", "")

if not DATABASE_URL:
    fail("DATABASE_URL is not set. Set it and re-run.")
    sys.exit(1)

# Railway sometimes provides postgres:// — SQLAlchemy needs postgresql://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    warn("Rewrote postgres:// → postgresql:// for SQLAlchemy compatibility.")

info(f"Connecting to: {DATABASE_URL[:45]}...")

# ── 2. Connect ──────────────────────────────────────────────────────────────
try:
    from sqlalchemy import create_engine, inspect, text
    engine = create_engine(DATABASE_URL, client_encoding="utf8")
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    ok("PostgreSQL connection successful.")
except Exception as e:
    fail(f"Connection failed: {e}")
    sys.exit(1)

# ── 3. Define all required tables and their columns ─────────────────────────
REQUIRED_TABLES = {
    # ── Migrated from MongoDB ────────────────────────────────────
    "served_users":     ["user_id"],
    "served_chats":     ["chat_id"],
    "pg_gban":          ["user_id", "reason"],
    "pg_afk":           ["user_id", "reason"],
    "pg_fsub":          ["chat_id", "channel"],
    "pg_couple":        ["chat_id", "date", "data"],
    "pg_karma":         ["chat_id", "user_key", "karma"],
    "pg_karma_toggle":  ["chat_id"],
    # ── Core SQLAlchemy tables (always existed) ──────────────────
    "users":            ["user_id"],
    "chats":            ["chat_id"],
    "gbans":            ["user_id"],
}

# ── 4. Create missing tables via the ORM ────────────────────────────────────
print(f"\n{BOLD}  Creating / verifying tables via SQLAlchemy ORM ...{RESET}\n")

try:
    # Temporarily point ENV so __init__.py won't crash if TOKEN is absent
    os.environ.setdefault("ENV", "True")
    os.environ.setdefault("API_ID", "0")
    os.environ.setdefault("API_HASH", "placeholder")
    os.environ.setdefault("TOKEN", "0:placeholder")
    os.environ.setdefault("OWNER_ID", "0")

    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy import Column, BigInteger, Integer, Text, UnicodeText

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
    ok("ORM create_all() completed (skips tables that already exist).")

except Exception as e:
    warn(f"ORM auto-create step raised: {e}")
    info("Continuing to inspection phase...")

# ── 5. Inspect what actually exists ─────────────────────────────────────────
print(f"\n{BOLD}  Inspecting table status ...{RESET}\n")

inspector = inspect(engine)
existing  = set(inspector.get_table_names())

all_ok    = True
for table, cols in REQUIRED_TABLES.items():
    if table in existing:
        ok(f"Table '{table}' exists.")
    else:
        fail(f"Table '{table}' is MISSING.")
        all_ok = False

# ── 6. Row-count sanity check for migrated tables ───────────────────────────
MIGRATED = ["served_users", "served_chats", "pg_gban", "pg_afk",
            "pg_fsub", "pg_couple", "pg_karma", "pg_karma_toggle"]

print(f"\n{BOLD}  Row counts for migrated tables:{RESET}\n")
try:
    with engine.connect() as conn:
        for table in MIGRATED:
            if table in existing:
                result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                count  = result.scalar()
                info(f"  {table:<22}  →  {count} row(s)")
            else:
                warn(f"  {table:<22}  →  (table missing, skipped)")
except Exception as e:
    warn(f"Row count query failed: {e}")

# ── 7. Final verdict ─────────────────────────────────────────────────────────
print(f"\n{BOLD}{'─'*55}{RESET}")
if all_ok:
    print(f"{BOLD}{GREEN}  ✔ All tables verified. Bot is ready for PostgreSQL.{RESET}")
    print(f"{BOLD}{'─'*55}{RESET}\n")
    sys.exit(0)
else:
    print(f"{BOLD}{RED}  ✖ Some tables are missing. Check the errors above.{RESET}")
    print(f"{BOLD}{'─'*55}{RESET}\n")
    sys.exit(1)
