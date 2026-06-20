# Django Telegram Bot Boilerplate (with UV)

A base project for building Telegram bots using **Django**, **Webhook**, and the ultra-fast **uv** package manager.

---

## 🚀 Overview

This project provides a clean and modular foundation for building Telegram bots using Django + Webhook.  
Features:

- Telegram bot integration with webhook architecture
- Separated handler system for commands, messages, callbacks, media
- Clean architecture using Django apps
- Environment variable support via `utils/load_env.py`
- Fast dependency management with [uv](https://github.com/astral-sh/uv)

---

## 📂 Project Structure

```text
.
├── apps/
│   ├── account/              # User models and logic
│   ├── bot/                  # Django views and bot-related logic
│   └── telegram/             # Telegram bot handlers & dispatcher
├── config/                   # Django settings and WSGI/ASGI config
├── utils/                    # Utility modules (env loader, logger, etc.)
├── uv.lock                   # uv lock file
├── pyproject.toml            # Project dependencies (PEP 621 compatible)
├── manage.py
└── README.md
```

## ⚙️ Installation & Setup

### 1. Prerequisites

- Python **3.11+**
- [`uv`](https://github.com/astral-sh/uv) installed:

```bash
curl -Ls https://astral.sh/uv/install.sh | sh
```
## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/base_telegram.git
cd base_telegram
```

---

### 2. Create Virtual Environment

```bash
uv venv
```

---

### 3. Install Dependencies

```bash
uv sync
```

# 🛠 Environment Configuration

After installing the required packages, create the environment configuration file:

```bash
cp .env.example .env
```

Then, the contents of the `.env` file should look like this:

---

## 🧩 `.env` File Structure

### ini
[DjangoSettings]
```
SECRET_KEY='django-insecure-noz+5u0cf1ym@fb$=rsgx0h+j)4rb(&x1e$-08a4=qqlo^5r4'
DEBUG=True
ALLOWED_HOSTS=
CSRF_TRUSTED_ORIGINS="https://your-ngrok-url.ngrok-free.app"
```

| Key                    | Description                                                                 |
|------------------------|-----------------------------------------------------------------------------|
| `SECRET_KEY`           | Django's secret key. Use a secure and private value in production.          |
| `DEBUG`                | Enables debug mode when set to $True$. Should be $False$ in production.     |
| `ALLOWED_HOSTS`        | Comma-separated list of hostnames your project can serve.                   |
| `CSRF_TRUSTED_ORIGINS` | List of trusted domains for CSRF protection (e.g., your ngrok or real domain). |

---

### $ini
[Proxy]
```
PROXY_SOCKS=127.0.0.1:2022
```

| Key           | Description                                                             |
|---------------|-------------------------------------------------------------------------|
| `PROXY_SOCKS` | SOCKS5 proxy address used to connect to Telegram (format: IP:PORT).     |

---

### $ini
[Bot]
```
BOT_NAME=BaseProject
TOKEN=5050400232:AAEeEApl-0geyNvmjfvW0ciInIubAiNS8Ck
BOT_USERNAME=graybot
BOT_USER_ID=5050400232
```

| Key             | Description                                                                 |
|------------------|-----------------------------------------------------------------------------|
| `BOT_NAME`       | Internal name or project name of the bot.                                   |
| `TOKEN`          | Telegram bot token obtained from BotFather. Keep this value confidential.   |
| `BOT_USERNAME`   | Telegram username of the bot.                                                |
| `BOT_USER_ID`    | Unique numeric ID of the bot.                                                |

---

### $ini
[Api]
```
FORCE_SCRIPT_NAME=/blind/
```

| Key                 | Description                                                                 |
|---------------------|-----------------------------------------------------------------------------|
| `FORCE_SCRIPT_NAME` | Used when deploying the project under a sub-path (e.g., $/blind/$).         |

---

# 🚀 How to Run the Project

To run the Django project using [**uv**](https://github.com/astral-sh/uv), follow these steps:

```bash
uv run manage.py makemigrations
uv run manage.py migrate
uv run manage.py runserver
```

### 📝 Explanation

| Command                           | Description                                              |
|-----------------------------------|----------------------------------------------------------|
| `uv run manage.py makemigrations` | Detect changes in models and prepare migration files.    |
| `uv run manage.py migrate`        | Apply migrations to the database.                        |
| `uv run manage.py runserver`      | Start the Django development server.                     |
