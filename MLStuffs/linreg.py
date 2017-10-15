print(__doc__)

import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
from data import Dataset

#configuration
config = {}

# Load the insurance dataset
dataset = Dataset(1000, 16)
insurance = dataset.load_dataset('train')


# Use only one feature
#insurance_X = insurance[:, np.newaxis, 2]

# Split the data into training/testing sets

insurance_X = []
insurance_y = []

for b, (sample, target) in enumerate(insurance):
	insurance_X.append(sample)
	insurance_y.append(target)

insurance_X_train = insurance[:-10000]
insurance_X_test = insurance[-10000:]

# Split the targets into training/testing sets
insurance_y_train = insurance[:-10000]
insurance_y_test = insurance[-10000:]

# Create linear regression object
regr = linear_model.LinearRegression()

# Train the model using the training sets
regr.fit(insurance_X_train, insurance_y_train)

# Make predictions using the testing set
insurance_y_pred = regr.predict(insurance_X_test)

# The coefficients
print('Coefficients: \n', regr.coef_)
# The mean squared error
print("Mean squared error: %.2f"
      % mean_squared_error(insurance_y_test, insurance_y_pred))
# Explained variance score: 1 is perfect prediction
print('Variance score: %.2f' % r2_score(insurance_y_test, insurance_y_pred))

# Plot outputs
plt.scatter(insurance_X_test, insurance_y_test,  color='black')
plt.plot(insurance_X_test, insurance_y_pred, color='blue', linewidth=3)

plt.xticks(())
plt.yticks(())

plt.show()