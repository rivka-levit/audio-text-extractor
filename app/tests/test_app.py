from unittest import TestCase

from app import app


class TestApp(TestCase):
    """Tests for the Flask app."""

    def setUp(self):
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()

    def tearDown(self):
        self.ctx.pop()

    def test_index_get(self):
        """Test index page get returns index.html"""

        header = 'Audio Text Extractor'

        r = self.client.get('/')

        self.assertEqual(r.status_code, 200)
        self.assertIn(header, r.get_data(as_text=True))
