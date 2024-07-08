# This file is adapted from the following source:
# Title: Replication package for the "DeepCrime: Mutation Testing of Deep Learning Systems based on Real Faults" paper
# Authors: Nargiz Humbatova, Gunel Jahangirova, & Paolo Tonella
# Conference: ACM SIGSOFT International Symposium on Software Testing and Analysis (ISSTA), Aarhus, Denmark
# Link: https://zenodo.org/records/4772465
# DOI: https://doi.org/10.5281/zenodo.4772465
# License: Creative Commons Attribution 4.0 International


from tensorflow.keras.utils import Sequence
from test_models.utils import IMAGE_HEIGHT, IMAGE_WIDTH, IMAGE_CHANNELS, load_image, augment, preprocess
import numpy as np


class Generator(Sequence):

    def __init__(self, path_to_pictures, steering_angles, is_training, args):
        self.batch_size = args.batch_size
        self.path_to_pictures = path_to_pictures
        self.steering_angles = steering_angles
        self.is_training = is_training
        self.args = args

    def __getitem__(self, index):
        start_index = index * self.batch_size
        end_index = start_index + self.batch_size
        batch_paths = self.path_to_pictures[start_index:end_index]
        steering_angles = self.steering_angles[start_index:end_index]

        images = np.empty([len(batch_paths), IMAGE_HEIGHT, IMAGE_WIDTH, IMAGE_CHANNELS])
        steers = np.empty([len(batch_paths)])
        for i, paths in enumerate(batch_paths):
            center, left, right = batch_paths[i]
            steering_angle = steering_angles[i]

            # augmentation
            if self.is_training and np.random.rand() < 0.6:
                image, steering_angle = augment(self.args.data_dir, center, left, right, steering_angle)
            else:
                image = load_image(self.args.data_dir, center)

            # add the image and steering angle to the batch
            images[i] = preprocess(image)
            steers[i] = steering_angle
        return images, steers

    def __len__(self):
        return len(self.path_to_pictures) // self.batch_size
