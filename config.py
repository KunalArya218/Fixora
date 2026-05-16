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
    SECRET_KEY = os.getenv("SECRET_KEY", "fixora-secret-key")

    # =========================
    # DATABASE (NEON / POSTGRES)
    # =========================
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME")

    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        f"?sslmode=require"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # =========================
    # MAIL CONFIG
    # =========================
    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "True") == "True"
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL", "False") == "True"

    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

    MAIL_DEFAULT_SENDER = os.getenv(
        "MAIL_DEFAULT_SENDER",
        MAIL_USERNAME
    )

    # =========================
    # FILE UPLOAD LIMIT (50MB)
    # =========================
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024

    # =========================
    # SECURITY SETTINGS
    # =========================
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    # =========================
    # IMPORTANT: PRODUCTION SAFETY
    # =========================
    DEBUG = False