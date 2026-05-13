import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "my_super_secret_password"
DB_NAME = "task_manager"

SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key")
