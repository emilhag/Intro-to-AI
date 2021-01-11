# save the final model to file
from keras.datasets import mnist
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Dense
from keras.layers import Flatten
from keras.optimizers import SGD
import numpy as np

# load train and test dataset
def load_dataset(n):
	# load dataset
	(trainX, trainY), (testX, testY) = mnist.load_data()
	# reshape dataset to have a single channel
	trainX = trainX.reshape((trainX.shape[0], 28, 28, 1))
	testX = testX.reshape((testX.shape[0], 28, 28, 1))
	print(trainX.shape)
	# one hot encode target values
	trainY = to_categorical(trainY)
	testY = to_categorical(testY)
	#subsample datapoints
	index = np.random.choice(trainX.shape[0], n, replace=False)
	trainX=trainX[index]
	#index=np.random.choice(trainY.shape[0], n, replace=False)
	trainY=trainY[index]
	print(trainX.shape)
	print(trainY.shape)
	return trainX, trainY, testX, testY

# scale pixels
def prep_pixels(train, test):
	# convert from integers to floats
	train_norm = train.astype('float32')
	test_norm = test.astype('float32')
	# normalize to range 0-1
	train_norm = train_norm / 255.0
	test_norm = test_norm / 255.0
	# return normalized images
	return train_norm, test_norm

# define cnn model
def define_model():
	model = Sequential()
	model.add(Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_uniform', input_shape=(28, 28, 1)))
	model.add(MaxPooling2D((2, 2)))
	#model.add(Conv2D(64, (3, 3), activation='relu', kernel_initializer='he_uniform'))
	# model.add(Conv2D(64, (3, 3), activation='relu', kernel_initializer='he_uniform'))
	# model.add(MaxPooling2D((2, 2)))
	model.add(Flatten())
	model.add(Dense(100, activation='relu', kernel_initializer='he_uniform'))
	model.add(Dense(10, activation='softmax'))
	# compile model
	opt = SGD(lr=0.01, momentum=0.9)
	model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])
	return model

# run the test harness for evaluating a model
def run_test_harness():
	print("loading dataset...")
	# load dataset
	n=30000 #training datapoints
	trainX, trainY, testX, testY = load_dataset(n)
	# prepare pixel data
	print("prep_pixels...")
	trainX, testX = prep_pixels(trainX, testX)
	# define model
	model = define_model()
	# fit model
	print("train model...")
	model.fit(trainX, trainY, epochs=10, batch_size=32, verbose=0)
	# save model
	model.save('model2.h5')

# entry point, run the test harness
run_test_harness()
