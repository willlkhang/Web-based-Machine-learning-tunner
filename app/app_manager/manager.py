import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from ML_models.mnist_number import load_data, MLP, MNISTModel
from database.job_model import Job

import torch.nn as nn 
import torch.optim as optim

import time
import datetime

class Manager:
    def __init__ (self, socketio):
        self.soketio = socketio

    def start_experiment(self, hyperparams):
        batch_size = hyperparams['batch_size']
        learning_rate = hyperparams['learning_rate']
        epochs = hyperparams['epochs']

        trainloader, testloader = load_data(batch_size)
        
        model = MLP()
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(model.parameters(), lr=learning_rate)
        mnistmodel = MNISTModel()

        start = time.time()
        mnistmodel.train_model(model, trainloader, criterion, optimizer, epochs, self.progress_update) #start training
        end = time.time()

        run_time = round(end-start, 3)
        
        accuracy = mnistmodel.evaluate_model(model, testloader)
        mnistmodel.save_model(model)

        Job.objects(epochs=epochs, 
                      learning_rate=learning_rate, 
                      batch_size=batch_size).update_one(set__status=True, 
                                                        set__time_finished=datetime.datetime.now(datetime.UTC), 
                                                        set__run_time=run_time, 
                                                        set__accuracy=accuracy)
        
        self.close_connection(hyperparams)
        
        return accuracy, run_time

    def progress_update(self, progress_data):
        self.soketio.emit('response', progress_data)

    def close_connection(self, hyperparams):
        self.soketio.emit('experiment_done', hyperparams)