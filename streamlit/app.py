import streamlit as st
import random
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler
import google.generativeai as genai
import pickle

def app():
    GOOGLE_API_KEY='AIzaSyAvtn3iiv_jbb8hGaebF7W9TH3BFuMe4-U'
    genai.configure(api_key=GOOGLE_API_KEY)

    st.set_page_config(page_title='Health Monitoring', layout='wide', page_icon=':hospital:')

    model_filename = 'D:/Dokumen/Mandiri/sic/gemini/health_status_model.h5'
    loaded_model = load_model(model_filename, compile=False)
    with open('D:/Dokumen/Mandiri/sic/gemini/scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)

    def predict_health_status(data):
        scaled_data = scaler.transform(data)
        predictions = loaded_model.predict(scaled_data)
        pred_class = np.argmax(predictions, axis=1)
        return pred_class[0]

    # Function to generate random metrics
    def generate_random_metrics():
        bpm = random.randint(60, 100)  # BPM (Heart Rate)
        spo2 = random.uniform(95, 100)  # SpO2 (Oxygen Saturation)
        temperature = random.uniform(36.0, 37.5)  # Body Temperature
        health_status = random.choice(["Sehat", "Sakit Ringan", "Sakit Parah"])  # Tingkat kesehatan tubuh
        return bpm, spo2, temperature, health_status

    def generate_recommendation(bpm, spo2, temperature, symptoms):

        model = genai.GenerativeModel('gemini-pro')

        prompt= f"Buatkan saran untuk pasien yang memiliki detak jantung per menit: {bpm} saturasi oksigen : {spo2} dan temperature: {temperature} dengan gejala {symptoms}"
        response = model.generate_content(prompt)
        result = ''.join([p.text for p in response.candidates[0].content.parts])
        return result

    # Judul aplikasi
    st.title('Health Metrics Dashboard')

    # Container untuk aplikasi
    with st.container( border=True):
        col1, col2, col3 = st.columns(3)

        # Tombol untuk memperbarui nilai metrik
        if st.button('Perbarui Metrik'):
            bpm, spo2, temperature, _ = generate_random_metrics()
            input_data = np.array([[bpm, temperature, spo2]]).reshape(1, -1)
            prediction = predict_health_status(input_data)
            health_status = "Sehat" if prediction == 0 else "Sakit Ringan" if prediction == 1 else "Sakit Parah"
        else:
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
            st.write(rekomendasi)

if __name__ == "__main__":
    app()
