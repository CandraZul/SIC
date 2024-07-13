import streamlit as st
import random
import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler
import requests

st.set_page_config(page_title='Health Monitoring', layout='wide', page_icon=':hospital:')

model_filename = 'health_status_model.pkl'
loaded_model = joblib.load(model_filename)

# Function to preprocess input data
def preprocess_input(data):
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(data)
    return scaled_data

# Function to predict health status
def predict_health_status(data):
    preprocessed_data = preprocess_input(data)
    predictions = loaded_model.predict(preprocessed_data)
    return predictions

# Function to generate random metrics
def generate_random_metrics():
    bpm = random.randint(60, 100)  # BPM (Heart Rate)
    spo2 = random.uniform(95, 100)  # SpO2 (Oxygen Saturation)
    temperature = random.uniform(36.0, 37.5)  # Body Temperature
    health_status = random.choice(["Sehat", "Sakit Ringan", "Sakit Parah"])  # Tingkat kesehatan tubuh
    return bpm, spo2, temperature, health_status

def generate_recommendation(bpm, spo2, temperature, symptoms):
    # Example of how to use Gemini API (replace with actual implementation)
    url = 'https://api.gemini.com'
    payload = {
        'bpm': bpm,
        'spo2': spo2,
        'temperature': temperature,
        'symptoms': symptoms
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer AIzaSyAvtn3iiv_jbb8hGaebF7W9TH3BFuMe4-U'  # Replace with your actual API key
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json().get('recommendation', 'No recommendation available')
    else:
        return f"Error: {response.status_code} - {response.text}"

# Judul aplikasi
st.title('Health Metrics Dashboard')
col1, col2, col3 = st.columns(3)

# Tombol untuk memperbarui nilai metrik
# Tombol untuk memperbarui nilai metrik
if st.button('Perbarui Metrik'):
    # Memanggil fungsi generate_random_metrics untuk mendapatkan nilai terbaru
    bpm, spo2, temperature, _ = generate_random_metrics()
    input_data = np.array([[bpm, temperature, spo2]])
    prediction = predict_health_status(input_data)
    health_status = "Sehat" if prediction == 0 else ("Sakit Ringan" if prediction == 1 else "Sakit Parah")
else:
    # Menampilkan metrik awal saat aplikasi pertama kali dijalankan
    bpm, spo2, temperature, health_status = generate_random_metrics()

# Menampilkan metric box untuk BPM (Beat Per Minute)
with col1:
    st.metric(label="BPM", value=bpm, delta=random.randint(-5, 5))

# Menampilkan metric box untuk SpO2 (Saturasi Oksigen)
with col2:
    st.metric(label="SpO2", value=f"{spo2:.1f}%", delta=f"{random.uniform(-1, 1):.1f}%")

# Menampilkan metric box untuk Suhu Tubuh
with col3:
    st.metric(label="Suhu Tubuh", value=f"{temperature:.1f} °C", delta=f"{random.uniform(-0.5, 0.5):.1f} °C")

# Menampilkan metric box untuk Tingkat Kesehatan
st.metric(label="Tingkat Kesehatan", value=health_status)

gejala = st.text_area("Masukkan gejala anda (opsional)", "")

if st.button('Buat Rekomendasi'):
    # Membuat rekomendasi berdasarkan data dan gejala
    rekomendasi = generate_recommendation(bpm, spo2, temperature, gejala)
    st.write("Rekomendasi:", rekomendasi)


