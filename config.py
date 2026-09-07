import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
BUSINESS_CONTEXT = """Sen PLAK INDUSTRIES'in Türkçe konuşan proje asistanısın. PLAK INDUSTRIES; endüstriyel tasarım, ürün geliştirme, CAD/CAM, prototipleme, üretime hazırlık, üretim yönlendirmesi, proje yönetimi ve mentorluk alanlarında destek sunan bir ürün geliştirme stüdyosudur.

Amacın ziyaretçinin ihtiyacını anlamak, ilgili hizmeti açıklamak ve uygun olduğunda ön görüşme için iletişim bırakmasını önermektir. Belgelerde bulunmayan fiyat, teslim tarihi, kapasite, adres, referans veya teknik güvence uydurma. Kesin teklif ve teknik kararların ekip değerlendirmesi gerektirdiğini belirt."""


def _csv_setting(name, default=""):
    return [item.strip() for item in os.getenv(name, default).split(",") if item.strip()]


class BaseConfig:
    SECRET_KEY = os.getenv("SECRET_KEY", "local-development-key")
    DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'plak_industries.db'}")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    AI_PROVIDER = os.getenv("AI_PROVIDER", "groq")
    AI_MODEL = os.getenv("AI_MODEL", "openai/gpt-oss-20b")
    AI_TIMEOUT_SECONDS = float(os.getenv("AI_TIMEOUT_SECONDS", "20"))
    ADMIN_SECRET = os.getenv("ADMIN_SECRET", "")
    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT", "587"))
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", "")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "")
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "true").lower() == "true"
    LEAD_NOTIFICATION_EMAIL = os.getenv("LEAD_NOTIFICATION_EMAIL", "plakendustri@gmail.com")
    CORS_ORIGINS = _csv_setting("CORS_ORIGINS", "http://127.0.0.1:5000,http://localhost:5000")
    BUSINESS_CONTEXT = BUSINESS_CONTEXT
    DEBUG = False
    TESTING = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class TestingConfig(BaseConfig):
    TESTING = True
    DEBUG = False
    DATABASE_URL = os.getenv("TEST_DATABASE_URL", "sqlite:///:memory:")
    ADMIN_SECRET = "test-admin-secret"


class ProductionConfig(BaseConfig):
    DEBUG = False


CONFIGS = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}


def validate_config(config_class):
    if config_class is ProductionConfig:
        missing = [name for name in ("SECRET_KEY", "ADMIN_SECRET") if not os.getenv(name)]
        if missing:
            raise RuntimeError(f"Üretim ayarları eksik: {', '.join(missing)}")


def get_config():
    environment = os.getenv("FLASK_ENV", "development").lower()
    return CONFIGS.get(environment, DevelopmentConfig)
