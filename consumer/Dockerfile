# Consumer
FROM python:3.9

RUN pip install --no-cache-dir pika kubernetes

WORKDIR /home/kacper/moje/roboczy/consumer/workfolder

COPY consumer.py .

CMD ["python", "consumer.py"]