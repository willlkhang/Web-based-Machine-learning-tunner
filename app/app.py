import pika
import json
import os
import sys

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

RABBITMQ_URL = "amqp://guest:guest@localhost:5672/"
params = pika.URLParameters(RABBITMQ_URL)

try:
    print("Connecting to Pika (Consumer)...")
    consumer_connection = pika.BlockingConnection(params)
    consumer_channel = consumer_connection.channel()
    consumer_channel.queue_declare(queue='task', durable=True)
    consumer_channel.basic_qos(prefetch_count=1)
    print("Consumer Connection successful")
except pika.exceptions.AMQPConnectionError as exc:
    print("RabbitMQ connection failed. No message sent")
    sys.exit(0)

def callback(ch, method, properties, body):
    body = json.loads(body)
    print(f"Received {body}")
    manager.start_experiment(body)
    ch.basic_ack(delivery_tag=method.delivery_tag)

consumer_channel.basic_consume(queue='task', on_message_callback=callback)
thread = Thread(target=consumer_channel.start_consuming, daemon=True) #running at the background
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

@app.post('/create-job')
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

            producer_connection = pika.BlockingConnection(params)
            producer_channel = producer_connection.channel()
            producer_channel.queue_declare(queue='task', durable=True)
            
            producer_channel.basic_publish(
                exchange='',
                routing_key='task',
                body=json.dumps(data),
                properties=pika.BasicProperties(delivery_mode=2) # make message persistent
            )
            
            # Close it immediately after sending
            producer_connection.close()

    except ValidationError as e:
        return make_response(jsonify({'message': str(e)}))
    
    job_json = job.to_json()
    response = make_response(
        jsonify({
            'message': message,
            'data': job_json
        }, 200)
    )

    return response

@app.get('/get-job')
def get_job():
    object = Job.objects.order_by("-accuracy").limit(10)
    response = make_response(jsonify({
        'message': 'Here are the best Arch Hyperparameters',
        'data': object.to_json()
    }))
    return response

@app.get('/find-job')
def find_job():
    epochs = int(request.args.get('epochs'))
    learning_rate = float(request.args.get('learning_rate'))
    batch_size = int(request.args.get('batch_size'))

    job = Job.objects(epochs=epochs, learning_rate=learning_rate, batch_size=batch_size).first()

    if job is None:
        return make_response(jsonify({
            'message': 'Job not found',
            'data': None
        }), 404) # Return a 404 Not Found status
    
    response = make_response(jsonify({
        'data': job.to_json()
    }))
    return response

if __name__ == '__main__':
    socketio.run(app, port=9000, allow_unsafe_werkzeug=True)