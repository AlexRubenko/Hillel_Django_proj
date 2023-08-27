from dj_config_url import parse
import psycopg2

url = "postgres://vuyxnphi:Ri5klwnxNX4NRYwV9etHpaqKut3XvHm2@trumpet.db.elephantsql.com/vuyxnphi"

db_config = parse(url)

try:
    conn = psycopg2.connect(
        dbname=db_config['NAME'],
        user=db_config['USER'],
        password=db_config['PASSWORD'],
        host=db_config['HOST'],
        port=db_config['PORT'],
    )

    print("Successfully connected to PostgreSQL!")
    conn.close()
except Exception as e:
    print("Connection to PostgreSQL failed:", e)
