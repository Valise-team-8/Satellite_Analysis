# 🛰️ Satellite Analysis — Land Use & Deforestation Detection

This project analyzes satellite images to classify land use and detect deforestation or afforestation over time.  
It uses **TensorFlow (CNN)** for land use classification and **OpenCV** for pixel-level deforestation analysis.  
A **Flask web app** provides a simple user interface to upload and visualize results.

---

## 🚀 Features

- 🧠 **Land Use Classification:**  
  Classifies satellite images into multiple land types (e.g., urban, forest, water, barren, etc.) using a trained CNN (`landuse_model.h5`).

- 🌳 **Deforestation Detection:**  
  Compares “before” and “after” satellite images to detect:

  - Deforestation (loss of vegetation)
  - Afforestation (increase in vegetation)
  - No major change

- 📊 **Model Performance Dashboard:**  
  Displays training metrics and class information.

- 💻 **Web Interface (Flask):**  
  Simple, responsive UI to upload images, view predictions, and see processing progress.

---

## 🧩 Project Structure

Satellite_Analysis/
│
├── app.py # Flask entry point
├── Train_model.py # Code for Retraining the model
├── dataset_extract.py # Prepareing Data For Training
│
├── templates/
│ ├── base.html # Common layout and navbar
│ ├── home.html # Common layout and navbar
│ ├── landuse.html # Land use upload & results
│ ├── deforestation.html # Deforestation comparison page
│ └── performance.html # Model performance display
│
├── static/
│ └── uploads/ # Uploaded user images
│
├── utils/
│ ├── preprocess.py # Image preprocessing helper
│ ├── predict.py # Prediction logic for CNN
│ └── deforestation.py # Pixel-based deforestation detection
│
├── models/
│ ├── landuse_model.h5 # Trained CNN model
│ └── class_names.json # Land use class labels
│
├── dataset_unprocessed/ # contains all the raw data used for training
├── dataset/ # Processed data used for training
│
├── requirements.txt # Dependencies
└── README.md # Project description

---

## ⚙️ Installation

```bash
### 1️⃣ Clone the Repository


git clone https://github.com/Valise-team-8/Satellite_Analysis.git
cd Satellite_Analysis

2️⃣ Create Virtual Environment

python -m venv venv
venv\Scripts\activate       # On Windows
# or
source venv/bin/activate    # On Linux/Mac

3️⃣ Install Dependencies

pip install -r requirements.txt

4️⃣ Run the Flask App

python app.py

Then open your browser at 👉 http://127.0.0.1:5000/


### How To Retrain Model?

1️⃣ Change dataset - optional

Change files in 'dataset_unprocessed' with images to to train

2️⃣ Extract Data

python dataset_extract.py


3️⃣ Train Model

python Train_model.py



🧠 Model Overview

The CNN model (landuse_model.h5) is trained using satellite image datasets.
It outputs probabilities for multiple land-use classes.
The model and class names are loaded dynamically from the models/ folder.
🌲 Deforestation Detection Logic

Deforestation and afforestation are differentiated using pixel brightness:

  🌳 Deforestation → Increase in brightness (vegetation loss → exposed soil)

  🌱 Afforestation → Decrease in brightness (soil covered by vegetation)

  ⚖️ No Major Change → Small difference (< threshold)

🧰 Tech Stack
Category	Technology
Language	Python 3
Framework	Flask
Machine Learning	TensorFlow / Keras
Image Processing	OpenCV, NumPy
Frontend/UI	Bootstrap 5

📷 Example Usage

  Upload a single image in Land Use to classify.

  Upload a pair of images (Before and After) in Deforestation to detect change.

  View results instantly with a simple progress spinner.


```
