from unittest import TestCase

from utils.extractor import AudioTextExtractor
from utils.mood import MoodAnalyzer


class TestMoodAnalyzer(TestCase):
    """Tests for analyzing mood of audio files."""

    def setUp(self):
        self.extractor = AudioTextExtractor()
        self.analyzer = MoodAnalyzer()

    def test_chile_audio_negative_text(self):
        """Test that the text of chile.wav is negative."""

        extracted_text = self.extractor.get_text('tests/chile.wav')
        mood = self.analyzer.get_mood(extracted_text)

        self.assertEqual(mood, 'Negative text...')
