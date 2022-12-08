import tensorflow as tf
from sklearn.utils import shuffle
import numpy as np
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras import models
from keras.callbacks import Callback
import random

noise = np.genfromtxt("../../bg.csv", delimiter = ',')
signal = np.genfromtxt("sig.csv", delimiter = ',')

noise = [i/4000 for i in noise]
signal = [i/4000 for i in signal]

signal_labels = []
noise_labels = []
for i in range(len(signal)):
    signal_labels.append(1)
for i in range(len(noise)):
    noise_labels.append(0)

# Join signal and background point and weight lists
all_points = np.concatenate((signal, noise))
all_labels = np.concatenate((signal_labels, noise_labels))

# Shuffle lists together
c = list(zip(all_points, all_labels))
random.shuffle(c)
all_points, all_labels = zip(*c)


# Define training data, training labels, test data, and test labels
test_fraction = 0.1
validation_fraction = 0.1


train_data = all_points[:int(len(all_points) * (1 - test_fraction))]
train_labels = all_labels[:int(len(all_points) * (1 - test_fraction))]
test_data = all_points[-int(len(all_points) * test_fraction):]
test_labels = all_labels[-int(len(all_labels) * test_fraction):]

# Vectorize data and labels
x_train = np.asarray(train_data).astype('float32')      # Vectorize training data
x_test = np.asarray(test_data).astype('float32')        # Vectorize test data

y_train = np.asarray(train_labels).astype('float32')    # Vectorize training labels
y_test = np.asarray(test_labels).astype('float32')      # Vectorize test labels

x_val = x_train[:int(len(x_train) * validation_fraction)]
partial_x_train = x_train[int(len(x_train) * validation_fraction):]

y_val = y_train[:int(len(y_train) * validation_fraction)]
partial_y_train = y_train[int(len(y_train) * validation_fraction):]

from keras.callbacks import EarlyStopping
early_stopping_monitor = EarlyStopping(patience=30)	#early stopping monitor to prevent over-training

def build_deep_model():
    deep_model = keras.models.Sequential()
    deep_model.add(layers.Input(shape=(6,)))
    deep_model.add(layers.Dense(300, activation='relu'))
    deep_model.add(layers.Dense(300, activation='relu'))
    deep_model.add(layers.Dense(300, activation='relu'))
    deep_model.add(layers.Dense(1, activation='sigmoid'))
    deep_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=[tf.keras.metrics.AUC()])
    return deep_model

#%%
# Run deep model
deep_model = build_deep_model()
deep_history = deep_model.fit(x_train, y_train, validation_split=0.1, batch_size = 32, epochs=200, callbacks=[early_stopping_monitor])

deep_model.save('Model')					#Saving the model for each signal hypothesis

##importing benchmark data and saving the network output on benchmark for running Bayesian Analysis
benchmark_data = np.genfromtxt('../../benchmark_dataset.csv', delimiter = ',')
benchmark_data = np.array([i/4000 for i in benchmark_data])
out = deep_model(benchmark_data).numpy()
np.savetxt('out_DL.csv', out, delimiter = ',')
									