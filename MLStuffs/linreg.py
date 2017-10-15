print(__doc__)

import math
import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
from data import Dataset
from sklearn.preprocessing import StandardScaler


# Load the insurance dataset
dataset = Dataset(432340, 16)
insurance = dataset.load_dataset('train')

# Use only one feature
#insurance_X = insurance[:, np.newaxis, 2]

# Split the data into training/testing sets

insurance_X = []
insurance_y = []

for b in insurance:
	#insurance_X.append([b[0][0].double(), b[0][1].double()])
	insurance_X.append([b[0][0][0], b[0][0][1]])
	insurance_y.append(b[1][0])


#insurance_X = insurance_X[:, np.newaxis, 7]

insurance_X_train = np.array(insurance_X[:-1500])
insurance_X_test = np.array(insurance_X[-1500:])

# Split the targets into training/testing sets
insurance_y_train = np.array(insurance_y[:-1500])
insurance_y_test = np.array(insurance_y[-1500:])

print("X count: ", len(insurance_X))
print("Y count: ", len(insurance_y))

sc = StandardScaler()
insurance_X_train = sc.fit_transform(insurance_X_train)
insurance_X_test = sc.transform(insurance_X_test)

# Create linear regression object
#regr = linear_model.LinearRegression()

from sklearn.tree import DecisionTreeClassifier

classifier = DecisionTreeClassifier(criterion = 'entropy', random_state = 0)
classifier.fit(insurance_X_train, insurance_y_train)

#insurance_X_train = insurance_X_train.reshape(-1, 1)
#insurance_y_train = insurance_y_train.reshape(-1, 1)

# Train the model using the training sets
#regr.fit(insurance_X_train, insurance_y_train)

# Make predictions using the testing set
insurance_y_pred = classifier.predict(insurance_X_test)

from sklearn.metrics import confusion_matrix

def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

cm = confusion_matrix(insurance_y_test, insurance_y_pred)

class_names = ["0", "1"]

#plot_confusion_matrix(cm, classes=class_names, title = 'Confusion Matrix, w/o Normalization, for HackRU')
# The coefficients
#print('Coefficients: \n',  classifier.coef_)
# The mean squared error

MSE = math.pow((cm[0,1] + cm[1,0])/(cm[0,0] + cm[0,1] + cm[1,0] + cm[1,1]),2)
print("Mean squared error: ", MSE)
# Explained variance score: 1 is perfect prediction
print('Variance score: %.2f' % r2_score(insurance_y_test, insurance_y_pred))

# Plot outputs
"""plt.scatter(insurance_X_test, insurance_y_test,  color='black')
plt.plot(insurance_X_test, insurance_y_pred, color='blue', linewidth=3)

plt.xticks(())
plt.yticks(())

plt.show()"""