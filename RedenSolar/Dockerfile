FROM python:3.6-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN mkdir /RedenSolar
WORKDIR /RedenSolar
RUN pip install --upgrade pip

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