import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-only-change-this-secret')
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # 2 MB per request
    DATA_PATH = str(BASE_DIR / 'data' / 'products.json')
    CONTACT_LOG = str(BASE_DIR / 'logs' / 'contacts.log')
    UPLOAD_FOLDER = str(BASE_DIR / 'app' / 'products' / 'static' / 'uploads')
    WTF_CSRF_ENABLED = True
