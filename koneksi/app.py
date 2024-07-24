import streamlit as st
import asyncio
from bleak import BleakClient, BleakScanner
import struct
import numpy as np
from keras.models import load_model
import pickle
import google.generativeai as genai
import time

st.set_page_config(page_title='Health Monitoring', layout='wide', page_icon=':hospital:')

# Define BLE Device Specs
DEVICE_NAME = 'ESP32'
BLE_SERVICE = "19b10000-e8f2-537e-4f6c-d104768a1214"
BPM_CHARACTERISTIC = '19b10001-e8f2-537e-4f6c-d104768a1214'
SPO2_CHARACTERISTIC = '19b10002-e8f2-537e-4f6c-d104768a1214'
TEMP_CHARACTERISTIC = '19b10003-e8f2-537e-4f6c-d104768a1214'

ble_state = st.empty()
bpm_value = st.empty()
spo2_value = st.empty()
temp_value = st.empty()
ble_server = None

def run_async(coro):
    """Run an asynchronous coroutine synchronously."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(coro)
    loop.close()
    return result

def connect_to_device():
    global ble_server
    ble_state.text('Initializing Bluetooth...')
    
    async def _connect():
        global ble_server  # Use global to modify the outer scope variable
        device = None

        # Discover devices
        devices = await BleakScanner.discover()
        for d in devices:
            if d.name == DEVICE_NAME:
                device = d
                break
        
        if device is None:
            ble_state.error("Device not found")
            return
        
        # Connect to the device
        ble_server = BleakClient(device)
        try:
            await ble_server.connect()
            ble_state.success(f"Connected to {device.name}")
        except Exception as e:
            ble_state.error(f"Failed to connect: {e}")
            return

    run_async(_connect())

def read_sensor_data():
    global bpm_value, spo2_value, temp_value, ble_server
    async def _read():
        while True:
            if ble_server:
                try:
                    bpm = await ble_server.read_gatt_char(BPM_CHARACTERISTIC)
                    spo2 = await ble_server.read_gatt_char(SPO2_CHARACTERISTIC)
                    temp = await ble_server.read_gatt_char(TEMP_CHARACTERISTIC)

                    decoded_bpm = int.from_bytes(bpm, byteorder='little')
                    decoded_spo2 = int.from_bytes(spo2, byteorder='little')
                    decoded_temp = struct.unpack('f', temp)[0]

                    bpm_value.text(f"BPM: {decoded_bpm}")
                    spo2_value.text(f"SpO2: {decoded_spo2}%")
                    temp_value.text(f"Temperature: {decoded_temp} °C")
                except Exception as e:
                    st.error(f"Error reading data: {e}")
            await asyncio.sleep(1)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(_read())
    finally:
        loop.close()

def predict_health_status(data):
    global loaded_model, scaler
    scaled_data = scaler.transform(data)
    predictions = loaded_model.predict(scaled_data)
    pred_class = np.argmax(predictions, axis=1)
    return pred_class[0]

def generate_recommendation(bpm, spo2, temperature, symptoms):
    model = genai.GenerativeModel('gemini-pro')

    prompt = f"Buatkan saran untuk pasien yang memiliki detak jantung per menit: {bpm}, saturasi oksigen: {spo2}, dan temperatur: {temperature} dengan gejala {symptoms}"
    response = model.generate_content(prompt)
    result = ''.join([p.text for p in response.candidates[0].content.parts])
    return result

def main():
    GOOGLE_API_KEY = 'YOUR_API_KEY_HERE'
    genai.configure(api_key=GOOGLE_API_KEY)

    global loaded_model, scaler
    model_filename = 'health_status_model.h5'
    loaded_model = load_model(model_filename, compile=False)
    with open('scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    
    st.title('Health Metrics Dashboard')

    # Container untuk aplikasi
    with st.container():
        col1, col2, col3 = st.columns(3)

        # Tombol untuk memperbarui nilai metrik
        if st.button('Connect to Device'):
            connect_to_device()
            if ble_server:
                read_sensor_data()

        # Menampilkan metric box untuk BPM (Beat Per Minute)
        with col1:
            st.metric(label="BPM", value=bpm_value.text if isinstance(bpm_value.text, str) else 'N/A')

        # Menampilkan metric box untuk SpO2 (Saturasi Oksigen)
        with col2:
            st.metric(label="SpO2", value=spo2_value.text if isinstance(spo2_value.text, str) else 'N/A')

        # Menampilkan metric box untuk Suhu Tubuh
        with col3:
            st.metric(label="Temperature", value=temp_value.text if isinstance(temp_value.text, str) else 'N/A')

        gejala = st.text_area("Masukkan gejala anda (opsional)", "")

        if st.button('Buat Rekomendasi'):
            # Membuat rekomendasi berdasarkan data dan gejala
            rekomendasi = generate_recommendation(bpm_value.text, spo2_value.text, temp_value.text, gejala)
            st.write(rekomendasi)

if __name__ == "__main__":
    main()
