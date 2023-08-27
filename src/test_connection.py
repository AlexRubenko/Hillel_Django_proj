import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import dev as settings
import psycopg2

db_settings = settings.DATABASES["default"]

try:
    conn = psycopg2.connect(
        dbname=db_settings["NAME"],
        user=db_settings["USER"],
        password=db_settings["PASSWORD"],
        host=db_settings["HOST"],
        port=db_settings["PORT"],
    )

    print("Successfully connected to PostgreSQL!")
    conn.close()
except Exception as e:
    print("Connection to PostgreSQL failed:", e)
