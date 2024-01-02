FROM python:3.12
LABEL authors="Rivka Levit"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./app /app

WORKDIR /app

EXPOSE 5000

RUN python -m pip install --upgrade pip && \
    python -m pip install nltk
RUN python -m nltk.downloader vader_lexicon
RUN pip install -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    mkdir -p /vol/web/media && \
    mkdir -p /vol/web/static && \
    chmod -R 755 /vol
