# MukeshRobot

A feature-rich, modular Telegram Group Management Bot written in Python.

## Overview

MukeshRobot is a powerful Telegram group management bot supporting:
- Group moderation (ban, mute, kick, warn, flood control)
- Welcome messages and rules
- Global bans (gban) enforcement
- Notes and filters
- Fun, info, and utility commands
- AI/ChatGPT integration via MukeshAPI
- Music management
- Federation management

## Architecture

- **Entry point**: `python3 -m MukeshRobot`
- **Framework**: `python-telegram-bot` v13.15 + `Pyrogram` v2.0.106 + `Telethon` v1.36.0
- **SQL Database**: PostgreSQL via SQLAlchemy (`DATABASE_URL`)
- **NoSQL Database**: MongoDB via PyMongo/Motor (`MONGO_DB_URI`)
- **Package manager**: pip (`requirements.txt`)
- **Python version**: 3.11

## Running Locally

1. Copy `.env.example` to `.env` and fill in all required values
2. Install dependencies: `pip install -r requirements.txt`
3. Start the bot: `python3 -m MukeshRobot`

## Required Environment Variables

| Variable | Required | Description |
|---|---|---|
| `ENV` | ✅ | Must be `True` to load from env vars |
| `TOKEN` | ✅ | Telegram bot token from @BotFather |
| `API_ID` | ✅ | Telegram API ID from my.telegram.org |
| `API_HASH` | ✅ | Telegram API Hash from my.telegram.org |
| `OWNER_ID` | ✅ | Your Telegram user ID (integer) |
| `DATABASE_URL` | ✅ | PostgreSQL connection URL |
| `MONGO_DB_URI` | ✅ | MongoDB connection URI |
| `EVENT_LOGS` | ✅ | Telegram channel ID for event logs |
| `SUPPORT_CHAT` | ✅ | Support group username |
| `START_IMG` | ✅ | Start image URL (Telegraph link) |

See `.env.example` for the full list of optional variables.

## Deployment (Railway)

See `railway.json` for Railway-specific configuration. Required services:
- **PostgreSQL** — for SQL data (federations, filters, warns, etc.)
- **MongoDB** — for NoSQL data (user/chat tracking, gbans)

## User Preferences

- Use pip for package management
- Keep modular structure intact
