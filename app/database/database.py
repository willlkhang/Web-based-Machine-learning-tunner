from mongoengine import connect, get_connection
import os

def connect_to_db():
    connect(host=os.getenv('MONGO_URL')) #map to the mongo db
    client = get_connection()
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
