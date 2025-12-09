import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from database.job_model import Job

import torch.nn as nn 
import torch.optim as optim

import time
import datetime

from MyTorch.MLP import MLP
from MyTorch.Trainer import Trainer
from MyTorch.MyData import MyData

class Manager:
    def __init__(self, socketio):
        self.socketio = socketio

    def start_experiment(self, hyperparams, dataset_name='mnist_number'):
        #dataset_name = hyperparams['dataset_name']
        batch_size = hyperparams['batch_size']
        learning_rate = hyperparams['learning_rate']
        epochs = hyperparams['epochs']

        dataset = MyData(dataset_name, batch_size)

        trainloader, testloader = dataset.loadDataset()

        model = MLP()

        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(model.parameters(), lr=learning_rate)

        path = './models/mnist_number.pth'

        mlp_trainer = Trainer(model, trainloader, testloader, criterion, optimizer, epochs, self.progress_update, path)

        start = time.time()
        mlp_trainer.train_model()
        end = time.time()

        run_time = round(end-start, 3)

        accuracy = mlp_trainer.evaluate_model()
        mlp_trainer.save_model()

        Job.objects(
                epochs=epochs, 
                learning_rate=learning_rate, 
                batch_size=batch_size
                    ).update_one(   
                            set__status=True, 
                            set__time_finished=datetime.datetime.now(datetime.UTC), 
                            set__run_time=run_time, 
                            set__accuracy=accuracy
                            )
        
        self.close_connection(hyperparams)

        return accuracy, run_time


    def progress_update(self, progress_data) -> None:
        self.socketio.emit('response', progress_data)

    def close_connection(self, hyperparams) -> None:
        self.socketio.emit('experiment_done', hyperparams)