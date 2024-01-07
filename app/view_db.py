import psycopg2
import os

from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    database=os.environ.get("DB_NAME"),
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASS"),
    host=os.environ.get("DB_HOST")
)
cursor = conn.cursor()
conn.autocommit = True

sql_cmd = 'SELECT * FROM audio'

cursor.execute(sql_cmd)
results = cursor.fetchall()
print(results)

cursor.close()
conn.close()
