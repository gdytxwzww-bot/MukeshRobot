# Python 3.11 Slim (matches runtime.txt)
FROM python:3.11-slim-bullseye

ENV PIP_NO_CACHE_DIR=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get upgrade -y && \
    apt-get install --no-install-recommends -y \
    bash \
    bzip2 \
    curl \
    figlet \
    ffmpeg \
    gcc \
    git \
    jq \
    libffi-dev \
    libjpeg-dev \
    libjpeg62-turbo-dev \
    libpq-dev \
    libwebp-dev \
    libxml2-dev \
    libxslt1-dev \
    libssl-dev \
    libreadline-dev \
    libyaml-dev \
    musl-dev \
    neofetch \
    openssl \
    postgresql-client \
    python3-dev \
    sqlite3 \
    libsqlite3-dev \
    unzip \
    wget \
    && rm -rf /var/lib/apt/lists/* /var/cache/apt/archives /tmp

# Upgrade pip and setuptools
RUN pip3 install --upgrade pip setuptools wheel

# Set working directory
WORKDIR /app

# Copy project files
COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

# Start the bot
CMD ["python3", "-m", "MukeshRobot"]
