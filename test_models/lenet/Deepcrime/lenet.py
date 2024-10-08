# This file is adapted from the following source:
# Title: Replication package for the "DeepCrime: Mutation Testing of Deep Learning Systems based on Real Faults" paper
# Authors: Nargiz Humbatova, Gunel Jahangirova, & Paolo Tonella
# Conference: ACM SIGSOFT International Symposium on Software Testing and Analysis (ISSTA), Aarhus, Denmark
# Link: https://zenodo.org/records/4772465
# DOI: https://doi.org/10.5281/zenodo.4772465
# License: Creative Commons Attribution 4.0 International

import numpy as np
import tensorflow as tf
import os
from sklearn.model_selection import train_test_split
from tensorflow.keras.layers import Input, Concatenate, Conv2D, Flatten, Dense, MaxPool2D
from tensorflow.keras.models import Model
from tensorflow.keras.initializers import RandomNormal, Constant, GlorotNormal
from tensorflow import math
from tensorflow.keras import backend as K

import matplotlib.pyplot as plt


def angle_loss_fn(y_true, y_pred):
    x_p = math.sin(y_pred[:, 0]) * math.cos(y_pred[:, 1])
    y_p = math.sin(y_pred[:, 0]) * math.sin(y_pred[:, 1])
    z_p = math.cos(y_pred[:, 0])

    x_t = math.sin(y_true[:, 0]) * math.cos(y_true[:, 1])
    y_t = math.sin(y_true[:, 0]) * math.sin(y_true[:, 1])
    z_t = math.cos(y_true[:, 0])

    norm_p = math.sqrt(x_p * x_p + y_p * y_p + z_p * z_p)
    norm_t = math.sqrt(x_t * x_t + y_t * y_t + z_t * z_t)

    dot_pt = x_p * x_t + y_p * y_t + z_p * z_t

    angle_value = dot_pt/(norm_p * norm_t)
    angle_value = tf.clip_by_value(angle_value, -0.99999, 0.99999)

    loss_val = (math.acos(angle_value))

    return tf.reduce_mean(loss_val, axis=-1)


def main(model_location):

    dataset_folder = os.path.join('Datasets', 'UnityEyes')

    x_img = np.load(os.path.join(dataset_folder, 'dataset_x_img.npy'))
    x_head_angles = np.load(os.path.join(dataset_folder, 'dataset_x_head_angles_np.npy'))
    y_gaze_angles = np.load(os.path.join(dataset_folder, 'dataset_y_gaze_angles_np.npy'))

    x_img_train, x_img_test, x_ha_train, x_ha_test, y_gaze_train, y_gaze_test = train_test_split(x_img, x_head_angles,
                                                                                                y_gaze_angles,
                                                                                                test_size=0.2,
                                                                                                random_state=42)


    if not (os.path.exists(model_location)):
        print("Training the model from scratch")
        # Build the model
        image_input = Input((36, 60, 1))
        head_pose_input = Input((2,))

        initialiser_normal = RandomNormal(mean=0., stddev=0.1)
        initialiser_const = Constant(value=0)
        initialiser_xavier = GlorotNormal(seed=None)

        x = Conv2D(filters=20,
                     kernel_size=(5, 5),
                     strides=1,
                     padding='valid',
                     kernel_initializer=initialiser_normal,
                     bias_initializer=initialiser_const,
                     activation='relu'
                   ) (image_input)

        x = MaxPool2D(strides=2, pool_size = 2) (x)

        x = Conv2D(filters=50,
                     kernel_size=(5, 5),
                     strides=1,
                     padding='valid',
                     kernel_initializer=initialiser_normal,
                     bias_initializer=initialiser_const,
                     activation='relu'
                   ) (x)

        x = MaxPool2D(strides=2, pool_size = 2) (x)

        x = Flatten() (x)
        # relu
        x = Dense(500,
                  activation='relu',
                  kernel_initializer=initialiser_xavier,
                  bias_initializer=initialiser_const,
                  ) (x)

        x = Concatenate()([head_pose_input, x])

        output = Dense(2) (x)

        model = Model(inputs = [image_input, head_pose_input], outputs = output)

        model.compile(
            optimizer = tf.keras.optimizers.SGD(),
            loss=angle_loss_fn,
            metrics=[angle_loss_fn],
        )

        history = model.fit([x_img_train, x_ha_train], y_gaze_train, batch_size=128, epochs=50, shuffle=True, validation_split=0.1, verbose=0)
        model.save(model_location)

        score = model.evaluate([x_img_test, x_ha_test], y_gaze_test, verbose=0)
        print("score:" + str(score))

        K.clear_session() # Clear the session to avoid memory leaks

        return score
    else:
        print("Loading the model from the saved location")
        graph1 = tf.Graph()
        with graph1.as_default():
            session1 = tf.compat.v1.Session()
            with session1.as_default():
                model = tf.keras.models.load_model(model_location, custom_objects={'angle_loss_fn': angle_loss_fn})
                score = model.evaluate([x_img_test, x_ha_test], y_gaze_test, verbose=0)
                print("score:" + str(score))
        
        K.clear_session() # Clear the session to avoid memory leaks
    
        return score



if (__name__ == '__main__'):
    score = main("")