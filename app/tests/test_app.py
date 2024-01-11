from unittest import TestCase

from app import app

import io


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

    def test_index_post_without_audio_return_error_page(self):
        """Test post to index page without audio redirects to error page."""

        r = self.client.post('/', follow_redirects=True,
                             content_type='multipart/form-data')

        expected_msg = 'No file part'
        expected_path = '/error'

        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.request.path, expected_path)
        self.assertIn(expected_msg, r.get_data(as_text=True))

    def test_index_post_with_empty_audio_name_return_error_page(self):
        """Test post to index page with empty audio name return error page."""

        data = {'audio': (io.BytesIO(b"abcdef"), '')}

        r = self.client.post('/', data=data, follow_redirects=True,
                             content_type='multipart/form-data')

        expected_msg = 'No selected file'
        expected_path = '/error'

        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.request.path, expected_path)
        self.assertIn(expected_msg, r.get_data(as_text=True))
