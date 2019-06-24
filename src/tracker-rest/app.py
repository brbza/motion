from kafka import KafkaConsumer
from kafka import KafkaProducer
from flask import Flask

topic = 'tracker'

app = Flask(__name__)
producer = KafkaProducer(bootstrap_servers='localhost:9092')


@app.route('/')
def hello():
    return 'Tracker REST!'


@app.route('/tracker')
def get_messages():
    messages = []
    for m in KafkaConsumer(topic, bootstrap_servers='localhost:9092'):
        messages.append(m)
    return '\n'.join(messages)
