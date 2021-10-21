FROM python:3.8

RUN apt-get update && \
  apt-get --yes install cmake && \
  rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

COPY src /app/src
COPY producer.py /app/producer.py

WORKDIR /app