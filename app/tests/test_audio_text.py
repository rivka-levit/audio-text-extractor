from unittest import TestCase

from utils.extractor import AudioTextExtractor


class TestAudioTextExtractor(TestCase):
    """Tests for extracting text from audio."""

    def setUp(self):
        self.extractor = AudioTextExtractor()

    def test_extract_text_from_wav_file(self):
        """Test extracting text from .wav file successfully."""

        t = self.extractor.get_text('tests/chile.wav')

        self.assertIsInstance(t, str)
