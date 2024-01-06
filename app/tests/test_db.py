import os
import psycopg2
from psycopg2.errors import DuplicateDatabase, DuplicateTable

from dotenv import load_dotenv

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
        result = self.cursor.fetchall()

        self.assertTrue(result)
