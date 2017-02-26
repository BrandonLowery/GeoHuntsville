FROM jfloff/alpine-python:2.7
RUN apk update && apk add python

ADD geohuntsville /app/geohuntsville
ADD requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

EXPOSE 8080

ENV PYTHONPATH /app
WORKDIR /app/geohuntsville

CMD ["python", "/app/geohuntsville/main.py"]
