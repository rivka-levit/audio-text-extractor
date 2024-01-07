import os

from flask import Flask, render_template, request, redirect

from utils.extractor import AudioTextExtractor
from utils.mood import MoodAnalyzer

import uuid

UPLOAD_FOLDER = '/vol/web/media'
ALLOWED_EXTENSIONS = {'wav'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')

    if request.method == 'POST':
        if 'audio' not in request.files:
            context = {'message': 'No file part'}
            return render_template('error.html', **context)

        audio = request.files['audio']

        if audio.filename == '':
            context = {'message': 'No selected file'}
            return render_template('error.html', **context)

        if audio and allowed_file(audio.filename):
            ext = audio.filename.rsplit('.', 1)[1]
            filename = f'{uuid.uuid4()}.{ext}'
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            audio.save(filepath)

            success, text = AudioTextExtractor().get_text(filepath)
            if success:
                mood = MoodAnalyzer().get_mood(text)
            else:
                mood = None

            context = {'text': text, 'mood': mood}
            return render_template('extract.html', **context)

        context = {'message': 'Invalid input!'}
        return render_template('error.html', **context)


@app.route('/error', methods=['GET'])
def error_page():
    return render_template('error.html')


@app.route('/extract', methods=['GET'])
def extract():
    return render_template('extract.html')
