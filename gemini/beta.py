import numpy as np
from tensorflow.keras.models import load_model
import pickle

# Load model and scaler
model_filename = 'D:/Dokumen/Mandiri/sic/gemini/health_status_model.h5'
loaded_model = load_model(model_filename)
with open('D:/Dokumen/Mandiri/sic/gemini/scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

def predict_health_status(data):
    scaled_data = scaler.transform(data)
    predictions = loaded_model.predict(scaled_data)
    pred_class = np.argmax(predictions, axis=1)
    return pred_class

# Generate different data points
data1 = np.array([83, 36.2, 96.8]).reshape(1, -1)
data2 = np.array([90, 37.0, 95.0]).reshape(1, -1)
data3 = np.array([70, 36.5, 98.0]).reshape(1, -1)

print(predict_health_status(data1)[0])
print(predict_health_status(data2)[0])
print(predict_health_status(data3)[0])

loaded_model.summary()
