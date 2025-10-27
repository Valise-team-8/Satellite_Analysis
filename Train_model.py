import tensorflow as tf
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from keras.optimizers import Adam
import matplotlib.pyplot as plt
import json
import os

# use non-interactive backend
import matplotlib

matplotlib.use("Agg")


# Dataset path
dataset_path = "dataset"
img_size = (128, 128)
batch_size = 32

# --- Load datasets ---
train_ds = tf.keras.utils.image_dataset_from_directory(
    dataset_path,
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=img_size,
    batch_size=batch_size,
)

val_ds = tf.keras.utils.image_dataset_from_directory(
    dataset_path,
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=img_size,
    batch_size=batch_size,
)

# --- Save class names and number of classes immediately ---
class_names = train_ds.class_names
num_classes = len(class_names)
print(f"Detected classes ({num_classes}): {class_names}")


# --- Normalize pixel values ---
normalization_layer = tf.keras.layers.Rescaling(1.0 / 255)
train_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
val_ds = val_ds.map(lambda x, y: (normalization_layer(x), y))

# --- Data Augmentation (Optional) ---
data_augmentation = tf.keras.Sequential(
    [tf.keras.layers.RandomFlip("horizontal"), tf.keras.layers.RandomRotation(0.2)]
)
train_ds = train_ds.map(lambda x, y: (data_augmentation(x, training=True), y))

AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.prefetch(buffer_size=AUTOTUNE)


# --- Fix number of classes ---
num_classes = len(class_names)

# --- Build CNN ---
model = Sequential(
    [
        Conv2D(
            32, (3, 3), activation="relu", input_shape=(img_size[0], img_size[1], 3)
        ),
        MaxPooling2D(2, 2),
        Conv2D(64, (3, 3), activation="relu"),
        MaxPooling2D(2, 2),
        Conv2D(128, (3, 3), activation="relu"),
        MaxPooling2D(2, 2),
        Flatten(),
        Dense(128, activation="relu"),
        Dropout(0.5),
        Dense(num_classes, activation="softmax"),  # ✅ Correct output layer
    ]
)


# --- Compile ---
model.compile(
    optimizer=Adam(learning_rate=0.001),
    loss="sparse_categorical_crossentropy",  # because labels are integers
    metrics=["accuracy"],
)

# --- Train ---
epochs = 15
history = model.fit(train_ds, validation_data=val_ds, epochs=epochs)

# --- Save model ---
model.save("model/landuse_model.h5")
print("✅ Model saved as model/landuse_model.h5")

# --- Save class names ---
with open("model/class_names.json", "w") as f:
    json.dump(class_names, f)
print("✅ Class names saved as model/class_names.json")

# --- Plot Accuracy & Loss and save to file ---
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(history.history["accuracy"], label="Train Accuracy")
plt.plot(history.history["val_accuracy"], label="Validation Accuracy")
plt.title("Accuracy")
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(history.history["loss"], label="Train Loss")
plt.plot(history.history["val_loss"], label="Validation Loss")
plt.title("Loss")
plt.legend()

os.makedirs("model", exist_ok=True)
plot_path = "model/training_plot.png"
plt.tight_layout()
plt.savefig(plot_path)
plt.close()
print(f"✅ Training plot saved to {plot_path}")
