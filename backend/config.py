import os
from dotenv import load_dotenv

load_dotenv()

def get_env_variable(var_name: str, default=None, is_mandatory: bool = True):
    value = os.getenv(var_name, default)
    if is_mandatory and value is None:
        raise ValueError(f"Mandatory environment variable '{var_name}' is missing.")
    return value

# Database credentials validated on startup
DB_HOST = get_env_variable("DB_HOST", "localhost")
DB_USER = get_env_variable("DB_USER", "root")
DB_PASSWORD = get_env_variable("DB_PASSWORD")
DB_NAME = get_env_variable("DB_NAME", "task_manager")

SECRET_KEY = get_env_variable("SECRET_KEY", "default-secret-key")

