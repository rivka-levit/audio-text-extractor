from unittest import TestCase

from utils.extractor import AudioTextExtractor


class TestAudioTextExtractor(TestCase):
    """Tests for extracting text from audio."""

    def setUp(self):
        self.extractor = AudioTextExtractor()

    def test_extract_text_from_wav_file(self):
        """Test extracting text from .wav file successfully."""

        success, text = self.extractor.get_text('tests/chile.wav')

        self.assertTrue(success)
        self.assertIsInstance(text, str)

    def test_audio_without_speech(self):
        """Test extracting text from audio without speech return warning."""

        expected_warn = 'The audio file does not contain any speech.'
        success, text = self.extractor.get_text('tests/music.wav')

        self.assertFalse(success)
        self.assertEqual(text, expected_warn)
