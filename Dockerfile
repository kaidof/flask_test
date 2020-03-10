FROM python:3.7.6-slim-stretch

LABEL maintainer="kaidof@yahoo.com"

RUN apt-get update -y && \
    apt-get install -y build-essential && \
    apt-get install -y --no-install-recommends -q \
        wget \
        curl \
        ca-certificates \
        libpq-dev \
        python-psycopg2

WORKDIR /app

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD [ "python", "app.py" ]
