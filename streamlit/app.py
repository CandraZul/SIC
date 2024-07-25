import streamlit as st
import asyncio
from bleak import BleakClient, BleakScanner
import time
import struct
import numpy as np
from keras.models import load_model
import pickle
import google.generativeai as genai

st.set_page_config(page_title='Health Monitoring', layout='wide', page_icon=':hospital:')

# Define BLE Device Specs
DEVICE_NAME = 'ESP32'
BLE_SERVICE = "19b10000-e8f2-537e-4f6c-d104768a1214"
BPM_CHARACTERISTIC = '19b10001-e8f2-537e-4f6c-d104768a1214'
SPO2_CHARACTERISTIC = '19b10002-e8f2-537e-4f6c-d104768a1214'
TEMP_CHARACTERISTIC = '19b10003-e8f2-537e-4f6c-d104768a1214'

GOOGLE_API_KEY='AIzaSyAvtn3iiv_jbb8hGaebF7W9TH3BFuMe4-U'
genai.configure(api_key=GOOGLE_API_KEY)

st.title('Health Metrics Dashboard')

# Use columns to align metrics horizontally
col1, col2, col3 = st.columns(3)


# Create placeholders for metrics

bpm_placeholder = col1.empty()
spo2_placeholder = col2.empty()
temp_placeholder = col3.empty()
health_placeholder = st.empty()

gejala = st.empty()

# Create a placeholder for BLE state and button
ble_state = st.empty()
button_placeholder = st.empty()

# Initialize values
health_status = "-"
ble_server = None
total_bpm, total_spo2, total_temp = 0, 0, 0
if 'record_status' not in st.session_state:
    st.session_state.record_status = False
if 'avg_bpm' not in st.session_state:
    st.session_state.avg_bpm = 0
if 'avg_spo2' not in st.session_state:
    st.session_state.avg_spo2 = 0
if 'avg_temp' not in st.session_state:
    st.session_state.avg_temp = 0
if 'health_status' not in st.session_state:
    st.session_state.health_status = "-"

bpm_placeholder.metric(label="BPM", value=st.session_state.avg_bpm)
spo2_placeholder.metric(label="SpO2", value=st.session_state.avg_spo2)
temp_placeholder.metric(label="Temperature", value=st.session_state.avg_temp)
health_placeholder.metric(label="Tingkat Kesehatan", value=st.session_state.health_status)

# Initialize health prediction
model_filename = 'streamlit/health_status_model.h5'
loaded_model = load_model(model_filename, compile=False)
with open('streamlit/scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

# Initialize session state
if 'connected' not in st.session_state:
    st.session_state.connected = False
if 'ble_status' not in st.session_state:
    st.session_state.ble_status = ""

def predict_health_status(data):
    scaled_data = scaler.transform(data)
    predictions = loaded_model.predict(scaled_data)
    pred_class = np.argmax(predictions, axis=1)
    return pred_class[0]

def generate_recommendation(bpm, spo2, temperature, symptoms):

    model = genai.GenerativeModel('gemini-pro')

    prompt= f"Buatkan saran untuk pasien yang memiliki detak jantung per menit: {bpm} saturasi oksigen : {spo2} dan temperature: {temperature} dengan gejala {symptoms}"
    response = model.generate_content(prompt)
    result = ''.join([p.text for p in response.candidates[0].content.parts])
    return result

async def connect_to_device():
    global ble_server
    st.session_state.ble_status = 'Initializing Bluetooth...'
    ble_state.text(st.session_state.ble_status)

    device = None

    # Discover devices
    devices = await BleakScanner.discover()
    for d in devices:
        if d.name == DEVICE_NAME:
            device = d
            break
    
    if device is None:
        st.session_state.ble_status = "Device not found"
        ble_state.text(st.session_state.ble_status)
        st.session_state.connected = False
        return
    
    # Connect to the device
    ble_server = BleakClient(device)
    try:
        await ble_server.connect()
        st.session_state.ble_status = f"Connected to {device.name}"
        st.session_state.connected = True
        ble_state.text("")
        await read_sensor_data()  # Start reading sensor data after connection

    except Exception as e:
        st.session_state.ble_status = f"Failed to connect: {e}"
        st.session_state.connected = False
        ble_state.text(st.session_state.ble_status)

async def read_sensor_data():
    global ble_server, total_bpm, total_spo2, total_temp
    record = False
    num = 0
    while st.session_state.connected:
        button_placeholder.empty()  # Remove the button after click
        if ble_server:
            try:
                bpm = await ble_server.read_gatt_char(BPM_CHARACTERISTIC)
                spo2 = await ble_server.read_gatt_char(SPO2_CHARACTERISTIC)
                temp = await ble_server.read_gatt_char(TEMP_CHARACTERISTIC)

                decoded_bpm = int.from_bytes(bpm, byteorder='little')
                decoded_spo2 = int.from_bytes(spo2, byteorder='little')
                
                if len(temp) == 4:  # Validate that the length of temp data is 4 bytes
                    decoded_temp = struct.unpack('f', temp)[0]
                else:
                    decoded_temp = 0.0  # Set a default value if data is invalid

                bpm_placeholder.metric(label="BPM", value=decoded_bpm)
                spo2_placeholder.metric(label="SpO2", value=decoded_spo2)
                temp_placeholder.metric(label="Temperature", value=decoded_temp)
                
                input_data = np.array([[decoded_bpm, decoded_temp, decoded_spo2]]).reshape(1, -1)
                prediction = predict_health_status(input_data)
                health_status = "Sehat" if prediction == 0 else "Sakit Ringan" if prediction == 1 else "Sakit Parah"
                health_placeholder.metric(label="Tingkat Kesehatan", value=health_status)

                if(decoded_bpm != 0 and decoded_spo2 != 0):
                    record = True
                if(record):
                    total_bpm += decoded_bpm
                    total_spo2 += decoded_spo2
                    total_temp += decoded_temp
                    num += 1
                if(num >= 50):
                    st.session_state.avg_bpm = total_bpm / num
                    st.session_state.avg_spo2 = total_spo2 / num
                    st.session_state.avg_temp = total_temp / num

                    st.write("Perekaman selesai")

                    bpm_placeholder.metric(label="BPM", value=st.session_state.avg_bpm)
                    spo2_placeholder.metric(label="SpO2", value=st.session_state.avg_spo2)
                    temp_placeholder.metric(label="Temperature", value=st.session_state.avg_temp)

                    input_data = np.array([[st.session_state.avg_bpm, st.session_state.avg_spo2, st.session_state.avg_temp]]).reshape(1, -1)
                    prediction = predict_health_status(input_data)
                    st.session_state.health_status = "Sehat" if prediction == 0 else "Sakit Ringan" if prediction == 1 else "Sakit Parah"
                    health_placeholder.metric(label="Tingkat Kesehatan", value=health_status)

                    st.write("Perekaman Selesai")
                    st.session_state.record_status = True
                    break
            except Exception as e:
                st.error(f"Error reading data: {e}")
        await asyncio.sleep(1)

# Display the button to connect to device if not connected
if not st.session_state.connected:
    with button_placeholder:
        if st.button("Connect to Device", key="connect_button"):
            # Run the async function
            asyncio.run(connect_to_device())
            
            # Check BLE status and update session state
            if 'Connected' in st.session_state.ble_status:
                
                st.session_state.connected = True
            else:
                st.session_state.connected = False
                st.rerun()  # Rerun the app to show the button again

# Display BLE status
# ble_state.text(st.session_state.ble_status)
if(st.session_state.record_status):
    input = gejala.text_area("Masukkan gejala anda (opsional)", "")

    if st.button('Buat Rekomendasi'):
        # Membuat rekomendasi berdasarkan data dan gejala
        rekomendasi = generate_recommendation(st.session_state.avg_bpm, st.session_state.avg_spo2, st.session_state.avg_temp, input)
        st.write(rekomendasi)