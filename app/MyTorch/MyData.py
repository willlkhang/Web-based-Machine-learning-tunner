import torch
from torchvision import datasets, transforms
import torch.nn as nn

from torch.utils.data import DataLoader, Dataset

# def load_data(batch_size=64):
#     transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,))])

#     trainset = datasets.MNIST(root='./data', train=True, download=True, transform=transform)
#     testset = datasets.MNIST(root='./data', train=False, download=True, transform=transform)

#     trainloader = DataLoader(trainset, batch_size=batch_size, shuffle=True)
#     testloader  = DataLoader(testset, batch_size=batch_size, shuffle=False)

#     return trainloader, testloader

class MyData():
    def __init__(self, dataset_name, batch_size=64):
        self.dataset_name = dataset_name
        self.batch_size = batch_size

        self.transform = transforms.Compose([
            transforms.ToTensor(), 
            transforms.Normalize((0.5,), (0.5,))
        ])

    def loadDataset(self):
        trainset, testset = None, None

        if self.dataset_name == "mnist_number":
            trainset = datasets.MNIST(root='./data', train=True, download=True, transform=self.transform)
            testset = datasets.MNIST(root='./data', train=False, download=True, transform=self.transform)
        elif self.dataset_name == "mnist_fashion":
            trainset = datasets.FashionMNIST(root='./data', train=True, download=True, transform=self.transform)
            testset = datasets.FashionMNIST(root='./data', train=False, download=True, transform=self.transform)

        trainloader = DataLoader(trainset, batch_size=self.batch_size, shuffle=True)
        testloader  = DataLoader(testset, batch_size=self.batch_size, shuffle=False)

        return trainloader, testloader