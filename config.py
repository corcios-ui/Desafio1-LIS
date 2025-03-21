import os

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "1234567890")
DB_NAME = os.getenv("DB_NAME", "sistema_financiero")
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "uploads/")
