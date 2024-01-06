import os
import psycopg2
from psycopg2.errors import DuplicateDatabase, DuplicateTable

from dotenv import load_dotenv

from datetime import datetime, timezone

from unittest import TestCase

load_dotenv()


class TestDatabase(TestCase):
    """Test database functionality."""

    def setUp(self):
        conn = psycopg2.connect(
            database=os.environ.get("DB_NAME"),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASS"),
            host=os.environ.get("DB_HOST")
        )
        cursor = conn.cursor()
        conn.autocommit = True
        try:
            cursor.execute('CREATE DATABASE test_audios')
        except DuplicateDatabase:
            pass
        cursor.close()
        conn.close()
        self.conn = psycopg2.connect(
            database='test_audios',
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASS"),
            host=os.environ.get("DB_HOST")
        )
        self.cursor = self.conn.cursor()
        self.conn.autocommit = True

    def tearDown(self):
        self.cursor.close()
        self.conn.close()
        conn = psycopg2.connect(
            database=os.environ.get("DB_NAME"),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASS"),
            host=os.environ.get("DB_HOST")
        )
        cursor = conn.cursor()
        conn.autocommit = True
        cursor.execute('DROP DATABASE test_audios')
        cursor.close()
        conn.close()

    def test_create_table(self):
        """Test creating table successfully."""

        sql_table = """CREATE TABLE test_audio (
        id SERIAL PRIMARY KEY,
        created_at TIMESTAMP NOT NULL,
        audio_file VARCHAR(255) NOT NULL,
        speech TEXT,
        mood VARCHAR(255))"""

        query = """SELECT EXISTS(
        SELECT * FROM pg_tables
        WHERE schemaname = 'public' AND tablename = 'test_audio');"""
        try:
            self.cursor.execute(sql_table)
        except DuplicateTable:
            pass
        self.cursor.execute(query)
        result = self.cursor.fetchone()

        self.assertTrue(result[0])


class TestAudioTable(TestCase):
    """Test recording data in audio table."""

    def setUp(self):
        conn = psycopg2.connect(
            database=os.environ.get("DB_NAME"),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASS"),
            host=os.environ.get("DB_HOST")
        )
        cursor = conn.cursor()
        conn.autocommit = True
        try:
            cursor.execute('CREATE DATABASE test_audios')
        except DuplicateDatabase:
            pass
        cursor.close()
        conn.close()
        self.conn = psycopg2.connect(
            database='test_audios',
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASS"),
            host=os.environ.get("DB_HOST")
        )
        self.cursor = self.conn.cursor()
        self.conn.autocommit = True

        sql_table = """CREATE TABLE test_audio (
        id SERIAL PRIMARY KEY,
        created_at TIMESTAMP NOT NULL,
        audio_file VARCHAR(255) NOT NULL,
        speech TEXT,
        mood VARCHAR(255))"""
        try:
            self.cursor.execute(sql_table)
        except DuplicateTable:
            pass

    def tearDown(self):
        self.cursor.execute('DROP TABLE test_audio')
        self.cursor.close()
        self.conn.close()
        conn = psycopg2.connect(
            database=os.environ.get("DB_NAME"),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASS"),
            host=os.environ.get("DB_HOST")
        )
        cursor = conn.cursor()
        conn.autocommit = True
        cursor.execute('DROP DATABASE test_audios')
        cursor.close()
        conn.close()

    def test_make_record_successfully(self):
        """Test creating audio record in database successfully."""

        data = {
            'dt': datetime.now(timezone.utc),
            'path': 'tests/chile.wav'
        }

        self.cursor.execute(
            """INSERT INTO test_audio (created_at, audio_file)
            VALUES (%s, %s)""",
            (data['dt'], data['path'])
        )

        query = """SELECT EXISTS(
        SELECT * FROM test_audio
        WHERE audio_file = 'tests/chile.wav')"""
        self.cursor.execute(query)
        result = self.cursor.fetchone()

        self.assertTrue(result[0])
