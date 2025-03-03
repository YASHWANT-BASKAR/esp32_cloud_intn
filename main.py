from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import numpy as np
import tensorflow as tf

app = FastAPI()

# Load the trained ML model (.h5 file)
model = tf.keras.models.load_model("model.h5")

# Define request structure
class ComplexData(BaseModel):
    real: List[float]
    imag: List[float]

# Function to convert a+ib to magnitude & phase
def process_complex_data(real, imag):
    complex_numbers = np.array(real) + 1j * np.array(imag)
    magnitude = np.abs(complex_numbers)
    phase = np.angle(complex_numbers)
    return magnitude.tolist(), phase.tolist()

@app.post("/process-data")
def process_data(data: ComplexData):
    magnitude, phase = process_complex_data(data.real, data.imag)

    # Prepare model input
    input_features = np.array([magnitude + phase]).reshape(1, -1)

    # Get prediction from ML model
    prediction = model.predict(input_features).tolist()

    return {"prediction": prediction}
