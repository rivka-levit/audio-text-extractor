# Audio Text Extractor
## Extract speech text from audio

#### The application works with .wav audio

Upload an audion file with extension .wav and get the text extracted and the 
mood of this text.

### Core Features:

- Frontend on Flask
- PostgreSQL database
- SpeechRecognition and nltk libraries
- Dockerized
- Unit tests

### Command to run the app in container:
```commandline
docker compose up
```

### Command to run tests:
```commandline
docker compose run --rm web sh -c "python -m unittest -v"
```
