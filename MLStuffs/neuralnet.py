import torch 
import torch.nn as nn
import torch.nn.functional as F

class FullyConnectedNet(nn.Module):
	def __init__(self):
		super(FullyConnectedNet, self).__init__()
		self.fc1 = nn.Linear(8, 40)
		self.fc2 = nn.Linear(40, 1)

	def forward(self, x):
		return F.softmax(self.fc2(F.relu(self.fc1(x))))