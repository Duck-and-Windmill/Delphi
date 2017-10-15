import argparse, os
from neuralnet import FullyConnectedNet
from train import Trainer


def main():

	parser = argparse.ArgumentParser()
	parser.add_argument('--epochs', '-e', type=int, default=10, help='Number of training epoches')
	parser.add_argument('--batch', '-b', type=int, default=16, help='Size of batches')
	parser.add_argument('--samples', '-s', type=int, default=1000, help='Number of samples')
	parser.add_argument('--lr', '-l', type=float, default=0.001, help='Learning rate')
	args = parser.parse_args()

	if not os.path.exists('save/'):
		os.mkdir('save/')

	if args.batch > args.samples:
		raise Exception("Batch size cannot be larger than total number of samples in dataset")

	if type(args.epochs) != int:
		raise Exception("Epochs number be an integer. Given "+str(type(args.epoches)))

	if args.samples < 1000:
		raise Exception("Insufficient training data. Sample size %d < 1000" %args.samples)

	train_config = {'epochs': args.epochs, 'batches': args.batch, 'samples':args.samples, 'lr': args.lr}

	model = FullyConnectedNet()

	t = Trainer(model, train_config)
	t.train()

if __name__ == '__main__':
    main()