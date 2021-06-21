FROM python:3.8.5

RUN mkdir /app

COPY requirements.txt /app

RUN pip3 install -r /app/requirements.txt

COPY . /app

WORKDIR /app

CMD gunicorn cloudblue.wsgi:application --bind 0.0.0.0:8000
