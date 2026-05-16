import os
from dotenv import load_dotenv

# =========================
# LOAD ENV VARIABLES
# =========================

load_dotenv()

# =========================
# CONFIG CLASS
# =========================

class Config:

    # =========================
    # SECRET KEY
    # =========================

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "fixora-secret-key"
    )

    # =========================
    # DATABASE CONFIG
    # =========================

    database_url = os.getenv(
        "DATABASE_URL"
    )

    # Fix old postgres:// issue
    if database_url and database_url.startswith(
        "postgres://"
    ):

        database_url = database_url.replace(
            "postgres://",
            "postgresql://",
            1
        )

    SQLALCHEMY_DATABASE_URI = database_url

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # =========================
    # MAIL CONFIG
    # =========================

    MAIL_SERVER = os.getenv(
        "MAIL_SERVER",
        "smtp.gmail.com"
    )

    MAIL_PORT = int(
        os.getenv(
            "MAIL_PORT",
            587
        )
    )

    MAIL_USE_TLS = str(os.getenv("MAIL_USE_TLS", "True")).strip().lower() in ["true", "1", "yes"]
    MAIL_USE_SSL = str(os.getenv("MAIL_USE_SSL", "False")).strip().lower() in ["true", "1", "yes"]

    MAIL_USERNAME = os.getenv(
        "MAIL_USERNAME"
    )

    MAIL_PASSWORD = os.getenv(
        "MAIL_PASSWORD"
    )

    MAIL_DEFAULT_SENDER = os.getenv(
        "MAIL_DEFAULT_SENDER",
        MAIL_USERNAME
    )

    # =========================
    # FILE LIMIT
    # =========================

    MAX_CONTENT_LENGTH = (
        50 * 1024 * 1024
    )

    # =========================
    # SECURITY
    # =========================

    SESSION_COOKIE_HTTPONLY = True

    REMEMBER_COOKIE_HTTPONLY = True

    SESSION_COOKIE_SAMESITE = "Lax"

    # =========================
    # PRODUCTION
    # =========================

    DEBUG = False