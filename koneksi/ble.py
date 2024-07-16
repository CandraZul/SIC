import asyncio
import streamlit as st
from bleak import BleakScanner, BleakClient

# Fungsi untuk melakukan scanning perangkat BLE
async def scan_ble_devices():
    devices = await BleakScanner.discover()
    return devices

# Fungsi untuk terhubung ke perangkat BLE dan menerima data
async def connect_to_device(address, characteristic_uuid):
    async with BleakClient(address) as client:
        if await client.is_connected():
            st.write(f"Connected to {address}")
            while True:
                value = await client.read_gatt_char(characteristic_uuid)
                st.session_state['sensor_value'] = int.from_bytes(value, byteorder='little')
                await asyncio.sleep(1)

# Aplikasi Streamlit
def streamlit_app():
    st.title("BLE Device Scanner")

    if 'devices' not in st.session_state:
        st.session_state['devices'] = []

    if st.button("Scan for devices"):
        devices = asyncio.run(scan_ble_devices())
        st.session_state['devices'] = devices

    device_names = [f"{device.name} ({device.address})" for device in st.session_state['devices']]
    device_selection = st.selectbox("Select a device to connect", device_names)

    if device_selection:
        selected_device = st.session_state['devices'][device_names.index(device_selection)]
        address = selected_device.address
        characteristic_uuid = "00002a37-0000-1000-8000-00805f9b34fb"  # UUID dari characteristic yang ingin dibaca

        if st.button("Connect to device"):
            asyncio.run(connect_to_device(address, characteristic_uuid))

    sensor_value = st.session_state.get('sensor_value', 'No data')
    st.write(f"Sensor Value: {sensor_value}")

if __name__ == '__main__':
    streamlit_app()
