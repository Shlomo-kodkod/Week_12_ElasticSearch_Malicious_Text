FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

ENV NLTK_DATA=/usr/local/share/nltk_data
RUN python -m nltk.downloader -d /usr/local/share/nltk_data vader_lexicon

COPY app ./app
COPY data ./data

EXPOSE 8085

CMD ["python","-m","uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8085"]