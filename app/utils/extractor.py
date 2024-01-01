from speech_recognition import Recognizer, AudioFile


class AudioTextExtractor:
    """Extract text from audio."""

    def __init__(self):
        self.rcz = Recognizer()

    def get_text(self, filename):
        """Extract text."""

        with AudioFile(filename) as audio_file:
            audio = self.rcz.record(audio_file)

        return self.rcz.recognize_google(audio)
