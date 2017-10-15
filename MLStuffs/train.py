import os, torch 
from datetime import datetime
from data import Dataset
from torch.autograd import Variable
import torch.optim as optim

class Trainer(object):
	def __init__(self, model, config):
		self.model = model
		self.lr = config['lr']
		self.epochs = config['epochs']
		self.batches = config['batches']
		self.samples = config['samples']
		self.dataset = Dataset(self.samples, self.batches)

	def train(self):
		loss = []
		validation = []
		h = []
		t = []

		self.optimizer = optim.SGD(self.model.parameters(), lr=self.lr)

		for e in range(self.epochs):
			for b, (num, sex, marital_status, age, longitude, latitude, target) in enumerate(self.dataset.load_dataset('train')):

				num, sex, marital_status, age, longitude, latitude, target = Variable(num), Variable(sex), Variable(marital_status), Variable(age), Variable(longitude), Variable(latitude), Variable(target)

				optimizer.zero_grad()

				hypo = self.model(num, sex, marital_status, age, longitude, latitude)
				loss = self.model.loss(hypo, target)

				loss.backward()

				losses.append(loss.data.tolist()[0])

				optimizer.step()

			validate.append(self.validate())

		torch.save(self.model.state_dict(), os.path.join('save', datetime.now().strftime('%m-%d-%Y-%H-%M') + '.pth'))

		self.dataset.subplots_2D(2, 'Training', y_data_list=[losses, validate], subplt_titles=['Cumulative Loss', 'Validation'],
					   x_label=['Iterations', 'Epochs'],
					   y_label=['Cumulative Loss', 'Accuracy'])
		self.dataset.show('Binary Spiral')

	def validate(self):
		self.model.eval()
		losses = []
		correct = 0
		cumulative_loss = 0

		validation_set = self.dataset.load_dataset('validation')

		for data, target in validation_set:
			data, target = Variable(data, volatile=True), Variable(target)
			output = self.model(data)
			cumulative_loss += self.model.loss(output, target, size_average=False).data[0]
			losses.append(cumulative_loss)

			pred = output.data.max(1)[1]
			correct += pred.eq(target.data).sum()

		total = len(validation_set) * self.batches
		acc = 100. * correct / total

		return acc