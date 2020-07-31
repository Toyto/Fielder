FROM python:3

ADD requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /mnt

COPY . .

ENV FLASK_APP=app.py
EXPOSE 8000

CMD gunicorn -w 4 --bind=0.0.0.0:8000 app:app