import torch
import time
from torchvision import datasets, transforms
import torch.nn as nn
#import torch.nn.functional as F

def load_data(batch_size=64):
    transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,))])

    trainset = datasets.MNIST(root='./data', train=True, download=True, transform=transform)
    testset = datasets.MNIST(root='./data', train=False, download=True, transform=transform)

    trainloader = torch.utils.data.DataLoader(trainset, batch_size=batch_size, shuffle=True)
    testloader = torch.utils.data.DataLoader(testset, batch_size=batch_size, shuffle=False)
    
    return trainloader, testloader

# Define the Model
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()

        self.net = nn.Sequential(
            nn.Flatten(),

            nn.Linear(28*28, 256),
            nn.ReLU(inplace=True),
            nn.Linear(256, 128),
            nn.ReLU(inplace=True),
            nn.Linear(128, 64),
            nn.ReLU(inplace=True),
            nn.Linear(64, 10),

            nn.log_softmax(dim=1)
        )

    def forward(self, x):
        return self.net(x)

class MNISTModel:
    def __init__(self):
        pass

    def train_model(self, model, trainloader, criterion, optimizer, epochs, progress_update):
        start_time = time.time()  # Start time
        for epoch in range(epochs):
            running_loss = 0
            for batch_id, (images, labels) in enumerate(trainloader):
                images = images.view(images.shape[0], -1)
                optimizer.zero_grad()
                output = model(images)
                loss = criterion(output, labels)
                loss.backward()
                optimizer.step()
                running_loss += loss.item()
                trainloader_len = len(trainloader)
                progress_data = {
                    'epoch_number': f"Epoch [{epoch+1}/{epochs}]",
                    'completion_of_epoch': f"{round((batch_id + 1) / trainloader_len * 100, 3)}",
                    'time': f"{round(time.time() - start_time, 2)}",
                    'total_progress': f"{round((trainloader_len * epoch + batch_id + 1) / (trainloader_len * epochs) * 100, 3)}"
                }
                progress_update(progress_data)
        return


    def evaluate_model(self, model, testloader):
        correct = 0
        total = 0
        with torch.no_grad():
            for images, labels in testloader:
                images = images.view(images.shape[0], -1)
                outputs = model(images)
                _, predicted = torch.max(outputs, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()
        return 100 * correct / total  # Return accuracy

    def save_model(self, model, path='mnist_number.pth'):
        torch.save(model.state_dict(), path)

    def load_model(self, model, path='mnist_number.pth'):
        model.load_state_dict(torch.load(path))
