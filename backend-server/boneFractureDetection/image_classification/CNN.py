import lightning.pytorch as pl
import torch.nn as nn
import torch.optim as optim
import torchmetrics
import torchvision.models as models


class CNN(pl.LightningModule):
    def __init__(self):
        super(CNN, self).__init__()
        self.loss_fn = nn.CrossEntropyLoss()
        self.accuracy = torchmetrics.Accuracy(task="multiclass", num_classes=2)

        self.conv1 = nn.Conv2d(1, 3, kernel_size=3, padding=1, stride=1)
        self.model = models.resnet50(weights='ResNet50_Weights.DEFAULT')
        self.fc2 = nn.Linear(1000, 2)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.conv1(x)
        x = self.model(x)
        x = self.fc2(x)
        return self.sigmoid(x)

    def training_step(self, batch, batch_idx):
        loss, scores, y = self._common_step(batch, batch_idx)
        accuracy = self.accuracy(scores, y)
        self.log_dict({'train_loss': loss, 'train_accuracy': accuracy}, on_step=False, on_epoch=True, prog_bar=True)
        return loss

    def validation_step(self, batch, batch_idx):
        loss, scores, y = self._common_step(batch, batch_idx)
        accuracy = self.accuracy(scores, y)
        self.log_dict({'val_loss': loss, 'val_accuracy': accuracy}, on_step=False, on_epoch=True, prog_bar=False,
                      sync_dist=True)
        return loss

    def test_step(self, batch, batch_idx):
        loss, scores, y = self._common_step(batch, batch_idx)
        accuracy = self.accuracy(scores, y)
        self.log_dict({'test_loss': loss, 'test_accuracy': accuracy}, on_step=False, on_epoch=True)
        return loss

    def configure_optimizers(self):
        optimizer = optim.Adam(self.parameters(), lr=3e-4)
        return optimizer

    def _common_step(self, batch, batch_idx):
        x, y = batch
        scores = self.forward(x)
        loss = self.loss_fn(scores, y)
        return loss, scores, y
