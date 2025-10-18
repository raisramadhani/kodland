import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key-change-in-production"
    DATABASE_NAME = os.environ.get("DATABASE_NAME") or "quiz_app.db"

    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY") or "YOUR_API_KEY"
    WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/forecast"
    DEFAULT_CITY = "Jakarta"

    POINTS_PER_CORRECT_ANSWER = 10
    MAX_LEADERBOARD_ENTRIES = 10


class DevelopmentConfig(Config):
    DEBUG = True
    FLASK_ENV = "development"


class ProductionConfig(Config):
    DEBUG = False
    FLASK_ENV = "production"
    SESSION_COOKIE_SECURE = True

    SECRET_KEY = os.environ.get("SECRET_KEY")
    if not SECRET_KEY:
        raise ValueError("No SECRET_KEY set for production environment")


class TestingConfig(Config):
    TESTING = True
    DATABASE_NAME = ":memory:"
    SECRET_KEY = "test-secret-key"


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}
