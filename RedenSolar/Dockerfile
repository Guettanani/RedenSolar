FROM python:3.6-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN mkdir /RedenSolar
WORKDIR /RedenSolar

RUN pip install --upgrade pip
RUN pip install psycopg2-binary

# Installez les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

RUN apt-get update \
    && apt-get install -y libpq-dev

RUN pip install psycopg2

COPY requirements.txt /RedenSolar

RUN pip install -r requirements.txt
COPY . /RedenSolar


EXPOSE 8000
ENV PYTHONUNBUFFERED 1

#COPY ./entrypoint2.sh .

#RUN sed -i 's/\r//g' /RedenSolar/entrypoint2.sh

#RUN chmod +x /RedenSolar/entrypoint2.sh

#ENTRYPOINT ["./entrypoint2.sh"]

#ENTRYPOINT ["sh", "/RedenSolar/entrypoint2.sh"]