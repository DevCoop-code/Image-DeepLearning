from keras.models import Sequential
from keras.layers import Convolution2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
import numpy as np

categories = ["chair", "camera", "butterfly", "elephant", "flamingo"]
nb_classes = len(categories)

image_w = 64
image_h = 64
