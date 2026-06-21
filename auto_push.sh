#!/bin/bash
# ─────────────────────────────────────────────
#  auto_push.sh — Replit → GitHub Auto-Sync
#  Watches for file changes every 30 seconds
#  and pushes them automatically.
# ─────────────────────────────────────────────

set -euo pipefail

# ── Git identity ──────────────────────────────
git config --global user.email "replit-autosync@bot.local"
git config --global user.name "Replit AutoSync"

# ── Credential helper using GITHUB_TOKEN ──────
if [ -z "${GITHUB_TOKEN:-}" ]; then
    echo "[AutoSync] ✖ GITHUB_TOKEN is not set. Cannot push to GitHub."
    exit 1
fi

git config --global credential.helper store
echo "https://oauth2:${GITHUB_TOKEN}@github.com" > ~/.git-credentials
chmod 600 ~/.git-credentials

# ── Ensure remote origin is correct ───────────
REPO_URL="https://github.com/gdytxwzww-bot/MukeshRobot.git"
git remote set-url origin "$REPO_URL"

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║      Replit → GitHub Auto-Sync Active    ║"
echo "║   Checking for changes every 30 seconds  ║"
echo "╚══════════════════════════════════════════╝"
echo ""

while true; do
    sleep 30

    # Collect untracked + modified + staged files
    MODIFIED=$(git --no-optional-locks diff --name-only 2>/dev/null)
    STAGED=$(git --no-optional-locks diff --staged --name-only 2>/dev/null)
    UNTRACKED=$(git --no-optional-locks ls-files --others --exclude-standard 2>/dev/null)

    if [ -n "$MODIFIED" ] || [ -n "$STAGED" ] || [ -n "$UNTRACKED" ]; then
        TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
        echo "[AutoSync] 🔄 Changes detected at $TIMESTAMP"

        git add -A

        # Build a meaningful commit message (first 3 changed files)
        CHANGED_FILES=$(git --no-optional-locks diff --staged --name-only \
            | head -3 | paste -sd ', ' -)
        COMMIT_MSG="auto-sync [${TIMESTAMP}]: ${CHANGED_FILES}"

        if git commit -m "$COMMIT_MSG" 2>&1; then
            if git push origin main 2>&1; then
                echo "[AutoSync] ✔ Pushed successfully → github.com/gdytxwzww-bot/MukeshRobot"
            else
                echo "[AutoSync] ✖ Push FAILED — verify GITHUB_TOKEN has 'repo' write scope."
                echo "[AutoSync]   Re-check token at: https://github.com/settings/tokens"
            fi
        else
            echo "[AutoSync] ✖ Commit failed — possible conflict or empty diff."
        fi
    fi
done
