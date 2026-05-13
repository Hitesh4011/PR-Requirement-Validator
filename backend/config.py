import os
from dotenv import load_dotenv

load_dotenv()

# Database credentials pulled from environment
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME", "task_manager")

SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key")
