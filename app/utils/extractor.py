from speech_recognition import Recognizer, AudioFile
from speech_recognition.exceptions import UnknownValueError


class AudioTextExtractor:
    """Extract text from audio."""

    def __init__(self):
        self.rcz = Recognizer()

    def get_text(self, filename):
        """Extract text."""

        with AudioFile(filename) as audio_file:
            audio = self.rcz.record(audio_file)

        try:
            speech = self.rcz.recognize_google(audio)
            return True, speech

        except UnknownValueError:
            return False, 'The audio file does not contain any speech.'
