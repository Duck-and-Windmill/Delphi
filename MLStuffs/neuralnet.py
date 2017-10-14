import torch 
import torch.nn as nn
import torch.nn.Functional as Functional

def FullyConnectedNet(nn.Module):
	def __init__(self):
		super(FullyConnectedNet, self).__init__()
		self.fc1 = Linear(3, 40)
		self.fc2 = Linear(40, 1)

	def forward(self, x):
		return F.softmax(self.fc2(F.relu(self.fc1(x))))