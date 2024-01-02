from nltk.sentiment import SentimentIntensityAnalyzer


class MoodAnalyzer:

    analyzer = SentimentIntensityAnalyzer()

    def get_mood(self, text: str) -> str:
        """Return the mood description of the text."""

        mood = self.analyzer.polarity_scores(text)['compound']

        if mood < 0:
            return 'Negative text...'

        return 'Positive text!'
