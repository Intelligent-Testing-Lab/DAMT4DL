# This file is adapted from the following source:
# Title: Replication package for the "DeepCrime: Mutation Testing of Deep Learning Systems based on Real Faults" paper
# Authors: Nargiz Humbatova, Gunel Jahangirova, & Paolo Tonella
# Conference: ACM SIGSOFT International Symposium on Software Testing and Analysis (ISSTA), Aarhus, Denmark
# Link: https://zenodo.org/records/4772465
# DOI: https://doi.org/10.5281/zenodo.4772465
# License: Creative Commons Attribution 4.0 International

import pandas as pd
import numpy as np
from zipfile import ZipFile
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow import keras
from tensorflow.keras import layers
from pathlib import Path
import matplotlib.pyplot as plt
import os

EMBEDDING_SIZE = 50


class RecommenderNet(keras.Model):
    def __init__(self, num_users, num_movies, embedding_size, **kwargs):
        super(RecommenderNet, self).__init__(**kwargs)
        self.num_users = num_users
        self.num_movies = num_movies
        self.embedding_size = embedding_size
        self.user_embedding = layers.Embedding(
            num_users,
            embedding_size,
            embeddings_initializer="he_normal",
            embeddings_regularizer=keras.regularizers.l2(1e-6),
        )
        self.user_bias = layers.Embedding(num_users, 1)
        self.movie_embedding = layers.Embedding(
            num_movies,
            embedding_size,
            embeddings_initializer="he_normal",
            embeddings_regularizer=keras.regularizers.l2(1e-6),
        )
        self.movie_bias = layers.Embedding(num_movies, 1)

    def call(self, inputs):
        user_vector = self.user_embedding(inputs[:, 0])
        user_bias = self.user_bias(inputs[:, 0])
        movie_vector = self.movie_embedding(inputs[:, 1])
        movie_bias = self.movie_bias(inputs[:, 1])
        dot_user_movie = tf.tensordot(user_vector, movie_vector, 2)
        # Add all the components (including bias)
        x = dot_user_movie + user_bias + movie_bias
        # The sigmoid activation forces the rating to between 0 and 1
        return tf.nn.sigmoid(x)

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
    print('fp', os.getcwd())
    movielens_dir = os.path.join('Datasets', 'MovieRecommender', 'ml-latest-small')
    ratings_file = os.path.join(movielens_dir, "ratings.csv")
    df = pd.read_csv(ratings_file)

    user_ids = df["userId"].unique().tolist()
    user2user_encoded = {x: i for i, x in enumerate(user_ids)}
    userencoded2user = {i: x for i, x in enumerate(user_ids)}
    movie_ids = df["movieId"].unique().tolist()
    movie2movie_encoded = {x: i for i, x in enumerate(movie_ids)}
    movie_encoded2movie = {i: x for i, x in enumerate(movie_ids)}
    df["user"] = df["userId"].map(user2user_encoded)
    df["movie"] = df["movieId"].map(movie2movie_encoded)

    num_users = len(user2user_encoded)
    num_movies = len(movie_encoded2movie)
    df["rating"] = df["rating"].values.astype(np.float32)
    min_rating = min(df["rating"])
    max_rating = max(df["rating"])

    print("Number of users: {}, Number of Movies: {}, Min rating: {}, Max rating: {}".format(num_users, num_movies,
                                                                                             min_rating, max_rating))
    df = df.sample(frac=1, random_state=42)
    x = df[["user", "movie"]].values
    y = df["rating"].apply(lambda x: (x - min_rating) / (max_rating - min_rating)).values
    # Assuming training on 90% of the data and validating on 10%.
    train_indices = int(0.9 * df.shape[0])
    x_train, x_val, y_train, y_val = (
        x[:train_indices],
        x[train_indices:],
        y[:train_indices],
        y[train_indices:],
    )
    x_train, x_test, y_train, y_test = train_test_split(x_train, y_train, test_size=0.2, random_state=1)
    model = RecommenderNet(num_users, num_movies, EMBEDDING_SIZE)
    model.compile(
        loss=tf.keras.losses.BinaryCrossentropy(), optimizer=keras.optimizers.Adam(lr=0.001),
        metrics=[tf.keras.losses.BinaryCrossentropy()]
    )

    d_scores = []
    if not os.path.exists(model_location):
        print('Training the model from scratch')
        history = model.fit(
            x=x_train,
            y=y_train,
            batch_size=64,
            epochs=5,
            verbose=0,
            validation_data=(x_val, y_val),
        )
        os.mkdir(model_location)
        model.save_weights(os.path.join(model_location, 'movie_recomm_trained.h5py'))
        # score = model.evaluate(x_train, y_train, verbose=0)
        d_scores = evaluate_model(model, x_train, y_train)
    else:
        print('Loading the model from the saved location')
        model.load_weights(os.path.join(model_location, 'movie_recomm_trained.h5py'))
        # score = model.evaluate(x_train, y_train, verbose=0)
        d_scores = evaluate_model(model, x_train, y_train)

    print('length of d_scores', len(d_scores))
    return d_scores

if __name__ == "__main__":
    score = main('movie_recomm_trained.h5')