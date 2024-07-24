import streamlit as st
import asyncio
from bleak import BleakClient, BleakScanner
import struct

# Define BLE Device Specs
DEVICE_NAME = 'ESP32'
BLE_SERVICE = "19b10000-e8f2-537e-4f6c-d104768a1214"
BPM_CHARACTERISTIC = '19b10001-e8f2-537e-4f6c-d104768a1214'
SPO2_CHARACTERISTIC = '19b10002-e8f2-537e-4f6c-d104768a1214'
TEMP_CHARACTERISTIC = '19b10003-e8f2-537e-4f6c-d104768a1214'

# Streamlit UI
st.title("ESP32 Bluetooth Health Monitor")
ble_state = st.empty()
bpm_value = st.empty()
spo2_value = st.empty()
temp_value = st.empty()
ble_server = None

async def connect_to_device():
    global ble_server
    ble_state.text('Initializing Bluetooth...')
    
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

async def read_sensor_data():
    while True:
        if ble_server:
            try:
                bpm = await ble_server.read_gatt_char(BPM_CHARACTERISTIC)
                spo2 = await ble_server.read_gatt_char(SPO2_CHARACTERISTIC)
                temp = await ble_server.read_gatt_char(TEMP_CHARACTERISTIC)

                decoded_bpm = int.from_bytes(bpm, byteorder='little')
                decoded_spo2 = int.from_bytes(spo2, byteorder='little')
                decoded_temp = struct.unpack('f', temp)[0] 

                bpm_value.write(f"BPM: {decoded_bpm}")
                spo2_value.write(f"SpO2: {decoded_spo2}")
                temp_value.write(f"Temperature: {decoded_temp} °C")
            except asyncio.CancelledError:
                bpm_value.error("Read operation was cancelled.")
                spo2_value.error("Read operation was cancelled.")
                temp_value.error("Read operation was cancelled.")
                break
            except Exception as e:
                bpm_value.error(f"Error reading data: {e}")
                spo2_value.error(f"Error reading data: {e}")
                temp_value.error(f"Error reading data: {e}")
        await asyncio.sleep(1)

if st.button("Connect to ESP32"):
    try:
        asyncio.run(connect_to_device())
        if ble_server:
            asyncio.run(read_sensor_data())
    except Exception as e:
        st.error(f"An error occurred: {e}")
