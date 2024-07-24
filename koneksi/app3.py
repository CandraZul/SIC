import streamlit as st
import asyncio
from bleak import BleakClient, BleakScanner
import time
import struct

st.set_page_config(page_title='Health Monitoring', layout='wide', page_icon=':hospital:')

# Define BLE Device Specs
DEVICE_NAME = 'ESP32'
BLE_SERVICE = "19b10000-e8f2-537e-4f6c-d104768a1214"
BPM_CHARACTERISTIC = '19b10001-e8f2-537e-4f6c-d104768a1214'
SPO2_CHARACTERISTIC = '19b10002-e8f2-537e-4f6c-d104768a1214'
TEMP_CHARACTERISTIC = '19b10003-e8f2-537e-4f6c-d104768a1214'

st.title('Health Metrics Dashboard')

# Use columns to align metrics horizontally
col1, col2, col3 = st.columns(3)

# Create placeholders for metrics
bpm_placeholder = col1.empty()
spo2_placeholder = col2.empty()
temp_placeholder = col3.empty()

# Create a placeholder for BLE state and button
ble_state = st.empty()
button_placeholder = st.empty()

# Initialize values
bpm_value = 0
spo2_value = 0
temp_value = 0
ble_server = None

# Initialize session state
if 'connected' not in st.session_state:
    st.session_state.connected = False
if 'ble_status' not in st.session_state:
    st.session_state.ble_status = ""

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
        ble_state.text(st.session_state.ble_status)
        await read_sensor_data()  # Start reading sensor data after connection
        
    except Exception as e:
        st.session_state.ble_status = f"Failed to connect: {e}"
        st.session_state.connected = False
        ble_state.text(st.session_state.ble_status)

async def read_sensor_data():
    global bpm_value, spo2_value, temp_value, ble_server
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
ble_state.text(st.session_state.ble_status)
