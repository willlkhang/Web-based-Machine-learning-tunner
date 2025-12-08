import torch
import time

class Trainer :
    def __init__(self, model, trainloader, testloader, criterion, optimizer, epochs, progress_update, path):
        self.model = model

        self.trainloader = trainloader
        self.testloader = testloader
        self.criterion = criterion
        self.optimizer = optimizer
        self.epochs = epochs
        self.progress_update = progress_update
        self.path = path
        
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)

    def train_model(self) -> None:
        start_time = time.time()  # Start time
        self.model.train()

        for epoch in range(self.epochs):
            running_loss = 0
            
            for batch_id, (images, labels) in enumerate(self.trainloader):
                images, labels = images.to(self.device), labels.to(self.device)

                images = images.view(images.shape[0], -1)

                self.optimizer.zero_grad()
                output = self.model(images)
                loss = self.criterion(output, labels)
                loss.backward()
                self.optimizer.step()
                running_loss += loss.item()
                trainloader_len = len(self.trainloader)

                progress_data = {
                    'epoch_number': f"Epoch [{epoch+1}/{self.epochs}]",
                    'completion_of_epoch': f"{round((batch_id + 1) / trainloader_len * 100, 3)}",
                    'time': f"{round(time.time() - start_time, 2)}",
                    'total_progress': f"{round((trainloader_len * epoch + batch_id + 1) / (trainloader_len * self.epochs) * 100, 3)}"
                }
                
                self.progress_update(progress_data)
        return


    def evaluate_model(self) -> float:
        correct = 0
        total = 0
        self.model.eval()

        with torch.no_grad():
            for images, labels in self.testloader:
                images, labels = images.to(self.device), labels.to(self.device)

                images = images.view(images.shape[0], -1)

                outputs = self.model(images)
                _, predicted = torch.max(outputs, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()

        return 100 * correct / total  # Return accuracy

    def save_model(self):
        torch.save(self.model.state_dict(), self.path)

    def load_model(self):
        self.model.load_state_dict(torch.load(self.path, map_location=self.device))
