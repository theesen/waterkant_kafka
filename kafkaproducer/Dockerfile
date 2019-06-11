FROM python:3.7-slim
WORKDIR /kafkaproducer

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "-u", "producer/main.py"]