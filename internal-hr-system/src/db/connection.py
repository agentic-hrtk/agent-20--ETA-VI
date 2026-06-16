"""Database connection pool — NexaCorp HR System."""
import os
import psycopg2
from psycopg2 import pool

DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "hr-db-prod.nexacorp.internal"),
    "port": int(os.environ.get("DB_PORT", 5432)),
    "database": os.environ.get("DB_NAME", "hr_system_prod"),
    "user": os.environ.get("DB_USER", "hr_app_user"),
    "password": os.environ.get("DB_PASSWORD"),
}

_pool = None

def get_pool():
    global _pool
    if _pool is None:
        _pool = psycopg2.pool.ThreadedConnectionPool(2, 20, **DB_CONFIG)
    return _pool

def get_conn():
    return get_pool().getconn()
