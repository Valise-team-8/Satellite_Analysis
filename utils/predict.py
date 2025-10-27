import tensorflow as tf
import numpy as np
from utils.preprocess import preprocess_image
import json

# Loading CNN Model
MODEL_PATH = "model/landuse_model.h5"
model = tf.keras.models.load_model(MODEL_PATH, compile=False)

# Label
with open("model/class_names.json") as f:
    class_names = json.load(f)


def predict_land_use(image_path):
    """
    Predict land use category of a satellite image.
    """
    img = preprocess_image(image_path)
    predictions = model.predict(img)
    predicted_class = class_names[np.argmax(predictions)]
    confidence = round(100 * np.max(predictions), 2)
    return predicted_class, confidence
