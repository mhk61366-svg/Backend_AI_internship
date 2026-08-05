import os
from pathlib import Path
from dotenv import load_dotenv
from psycopg import connect
from psycopg.rows import dict_row

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

HOST = os.getenv("POSTGRES_HOST", "localhost")
PORT = int(os.getenv("POSTGRES_PORT", "5432"))
DB_NAME = os.getenv("POSTGRES_DB", "backend_ai_internship")
USER = os.getenv("POSTGRES_USER", "postgres")
PASSWORD = os.getenv("POSTGRES_PASSWORD", "CHANGE_ME")
TABLE_NAME = os.getenv("POSTGRES_TABLE", "users")
DATABASE_URL = os.getenv("DATABASE_URL", "").strip()


def get_connection():
    conn_kwargs = {"row_factory": dict_row}

    if DATABASE_URL:
        return connect(DATABASE_URL, **conn_kwargs)

    return connect(
        host=HOST,
        port=PORT,
        dbname=DB_NAME,
        user=USER,
        password=PASSWORD,
        **conn_kwargs,
    )

def get_table_name():
    return TABLE_NAME
