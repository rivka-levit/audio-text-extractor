import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    database=os.environ.get("DB_NAME"),
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASS"),
    host=os.environ.get("DB_HOST")
)

cursor = conn.cursor()

sql_table = """CREATE TABLE audios (
id SERIAL PRIMARY KEY,
created_at TIMESTAMP NOT NULL,
audio_file VARCHAR(255) NOT NULL,
speech TEXT,
mood VARCHAR(255))"""

cursor.execute(sql_table)

conn.close()
