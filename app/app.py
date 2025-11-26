import json
import os
import pika

from flask import Flask, jsonify, request, make_response
from flask_socketio import SocketIO
from flask_cors import CORS

from app_manager.manager import Manager
from threading import Thread
from database.database import connect_to_db
from database.job_model import Job

from mongoengine import ValidationError
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")
manager = Manager(socketio)
load_dotenv()
connect_to_db()

try:
    print("Connectiong to Pika")
    params = pika.URLParameters("amqp://guest:guest@localhost:5672/")
    connection = pika.BlockingConnection(params)
except pika.exceptions.AMQPConnectingError as exc:
    print("RabbitMQ connection failed. No message sent")

#Rabbit config
print("Connection successful")
channel = connection.channel()
channel.queue_declare(queue='task', durable=True)
channel.basic_qos(prefetch_count=1)

def callback(ch, method, properties, body):
    body = json.loads(body)
    print(f"Received {body}")
    manager.start_experiment(body)
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(queue='task', on_message_callback=callback)
thread = Thread(target=channel.start_consuming, daemon=True) #running at the background
thread.start()

def initialize_key(key):
    data = {'epochs': 5, 'bath_size': 64, 'learning_rate': 3e-3}
    try:
        if key == 'learning_rate':
            return float(request.json[key])
        else:
            return int(request.json[key])
    except:
        print(f'{key} key not found in request form. Using a default value of {data[key]}')
        return data[key]

@app.route('/')
def home():
    return "Hom API. This is Will's web"

@app.route('/create-job')
def create_job():
    data = {} #setup hyperparam
    data['epochs'] = initialize_key('epochs')
    data['batch_size'] = initialize_key('batch_size')
    data['learning_rate'] = initialize_key('learning_rate')

    try: #save data or fetch from database
        message, job = Job.create_or_get_job(epochs=data['epochs'], 
                                             learning_rate=data['learning_rate'],
                                             batch_size=data['batch_size'])
        if message == "New Architecture created and saved":
            print(f"Create job called with request: {data}")
            channel.basic_publish(
                exchange='',
                routing_key='task',
                body=json.dumps(data),
                properties=pika.BasicProperties(delivery_model=2) #make message persistent
            )
    except ValidationError as e:
        return make_response(jsonify({'message': e.message}))
    
    job_json = job.to_json()
    response = make_response(
        jsonify({
            'message': message,
            'data': job_json
        }, 200)
    )

    return response
