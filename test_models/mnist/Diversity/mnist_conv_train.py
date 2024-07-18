# This file is adapted from the following source:
# Title: Replication package for the "DeepCrime: Mutation Testing of Deep Learning Systems based on Real Faults" paper
# Authors: Nargiz Humbatova, Gunel Jahangirova, & Paolo Tonella
# Conference: ACM SIGSOFT International Symposium on Software Testing and Analysis (ISSTA), Aarhus, Denmark
# Link: https://zenodo.org/records/4772465
# DOI: https://doi.org/10.5281/zenodo.4772465
# License: Creative Commons Attribution 4.0 International

from __future__ import print_function
import keras, sys
import os
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K
import tensorflow as tf
import numpy as np


def evaluate_model(model, x_data, y_data):
    """
    Evaluate the model on single data of whole dataset
    """
    scores = []
    for i, (x,y) in enumerate(zip(x_data, y_data)):
        x_batch = x[np.newaxis, ...]
        y_batch = np.array([y])
        single_score = model.evaluate(x_batch, y_batch, verbose=0)
        scores.append([i, single_score[0], single_score[1]]) # index, score[0], score[1]
    return scores

def main(model_location):
    ((x_train, y_train), (x_test, y_test)) = mnist.load_data()
    (img_rows, img_cols) = (28, 28)
    num_classes = 10

    if K.image_data_format() == 'channels_first':
        x_train = x_train.reshape(x_train.shape[0], 1, img_rows, img_cols)
        x_test = x_test.reshape(x_test.shape[0], 1, img_rows, img_cols)
        input_shape = (1, img_rows, img_cols)
    else:
        x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 1)
        x_test = x_test.reshape(x_test.shape[0], img_rows, img_cols, 1)
        input_shape = (img_rows, img_cols, 1)

    x_train = x_train.astype('float32')
    x_test = x_test.astype('float32')
    x_train /= 255
    x_test /= 255
    # print('x_train shape:', x_train.shape)
    # print(x_train.shape[0], 'train samples')
    # print(x_test.shape[0], 'test samples')
    y_train = keras.utils.to_categorical(y_train, num_classes)
    y_test = keras.utils.to_categorical(y_test, num_classes)

    if (not os.path.exists(model_location)):
        print("Training the model from scratch")
        batch_size = 128 
        epochs = 12
        model = Sequential()
        model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=input_shape))
        model.add(Conv2D(64, (3, 3), activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))
        model.add(Flatten())
        model.add(Dense(128, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(num_classes, activation='softmax'))
        model.compile(loss=keras.losses.categorical_crossentropy, optimizer=keras.optimizers.Adadelta(learning_rate = 1.0), metrics=['accuracy'])
        model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, verbose=0, validation_data=(x_test, y_test))
        model.save(model_location)
        # score = model.evaluate(x_train, y_train, verbose=0)
        d_scores = evaluate_model(model, x_train, y_train)
        print("The length of the scores: %s" % len(d_scores))

        K.clear_session() # Clear the session to avoid memory leaks
        return d_scores
    else:
        print("Loading the model from the file")
        graph1 = tf.Graph()
        with graph1.as_default():
            session1 = tf.compat.v1.Session()
            with session1.as_default():
                model = tf.keras.models.load_model(model_location)
                # score = model.evaluate(x_train, y_train, verbose=0)
                d_scores = evaluate_model(model, x_train, y_train)
                print("The length of the scores: %s" % len(d_scores))
        
        K.clear_session() # Clear the session to avoid memory leaks
        return d_scores

if __name__ == '__main__':
    score = main('')
