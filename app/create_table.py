import os

import psycopg2
from psycopg2.errors import DuplicateDatabase, DuplicateTable

from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    database='postgres',
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASS"),
    host=os.environ.get("DB_HOST")
)

cursor = conn.cursor()
conn.autocommit = True
try:
    cursor.execute('CREATE DATABASE audios')
except DuplicateDatabase:
    pass
cursor.close()
conn.close()

conn = psycopg2.connect(
    database=os.environ.get("DB_NAME"),
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASS"),
    host=os.environ.get("DB_HOST")
)
cursor = conn.cursor()
conn.autocommit = True

sql_table = """CREATE TABLE audio (
id SERIAL PRIMARY KEY,
created_at TIMESTAMP NOT NULL,
audio_file VARCHAR(255) NOT NULL,
speech TEXT,
mood VARCHAR(255))"""

try:
    cursor.execute(sql_table)
except DuplicateTable:
    pass

cursor.close()
conn.close()
