import psycopg2
import time
import os

from pathlib import Path
from dotenv import load_dotenv
from threading import Thread

load_dotenv()


def delete_old_records():
    """Delete records older than 15 minutes from db and from media folder."""

    while True:
        conn = psycopg2.connect(
            database='audios',
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASS"),
            host=os.environ.get("DB_HOST")
        )
        cursor = conn.cursor()
        conn.autocommit = True

        sql_cmd = """SELECT id, audio_file FROM audio 
        WHERE created_at + interval '15 minutes' <= NOW()"""

        cursor.execute(sql_cmd)
        old_records = cursor.fetchall()

        if old_records:
            for id_num, path in old_records:
                filepath = Path(path)
                with open(path, 'wb') as audio:
                    audio.write(b'')
                filepath.unlink()

                cursor.execute('DELETE FROM audio WHERE id = %s', (id_num,))

        cursor.close()
        conn.close()

        time.sleep(900)


if __name__ == "__main__":
    thread = Thread(target=delete_old_records, daemon=True)
    thread.start()
