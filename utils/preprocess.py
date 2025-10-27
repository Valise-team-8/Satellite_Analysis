import cv2
import numpy as np


def preprocess_image(image_path, target_size=(128, 128)):
    """
    Load and preprocess an image for the ML model.
    """
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, target_size)
    img = img / 255.0
    img = np.expand_dims(img, axis=0)
    return img
