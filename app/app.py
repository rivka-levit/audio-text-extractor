import os
import json

import psycopg2

from flask import Flask, render_template, request, redirect, url_for

from datetime import datetime, timezone
from pathlib import Path

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


def write_to_db(fpath, text, mood) -> None:
    """Save record to database."""

    conn = psycopg2.connect(
        database=os.environ.get("DB_NAME"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASS"),
        host=os.environ.get("DB_HOST")
    )
    cursor = conn.cursor()
    conn.autocommit = True

    sql = """INSERT INTO audio (created_at, audio_file, speech, mood) 
    VALUES (%s, %s, %s, %s)"""

    cursor.execute(
        sql,
        (datetime.now(timezone.utc), fpath, text, mood)
    )

    cursor.close()
    conn.close()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')

    if request.method == 'POST':
        if 'audio' not in request.files:
            message = json.dumps({'message': 'No file part'})
            return redirect(url_for('error_page', message=message))

        audio = request.files['audio']

        if audio.filename == '':
            message = json.dumps({'message': 'No selected file'})
            return redirect(url_for('error_page', message=message))

        if audio and allowed_file(audio.filename):
            ext = audio.filename.rsplit('.', 1)[1]
            filename = f'{uuid.uuid4()}.{ext}'
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            audio.save(filepath)

            success, text = AudioTextExtractor().get_text(filepath)

            if success:
                mood = MoodAnalyzer().get_mood(text)
                write_to_db(filepath, text, mood)
            else:
                mood = None
                path = Path(filepath)
                with open(filepath, 'wb') as file:
                    file.write(b'')
                path.unlink()

            context = {'text': text, 'mood': mood}
            return render_template('extract.html', **context)

        context = {'message': 'Invalid input!'}
        return render_template('error.html', **context)


@app.route('/error', methods=['GET'])
def error_page():
    message = request.args.get('message', None)
    return render_template('error.html', message=json.loads(message))


@app.route('/extract', methods=['GET'])
def extract():
    return render_template('extract.html')
