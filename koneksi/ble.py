import streamlit as st
import asyncio
from bleak import BleakClient, BleakScanner

# Define BLE Device Specs
DEVICE_NAME = 'ESP32'
BLE_SERVICE = "19b10000-e8f2-537e-4f6c-d104768a1214"
LED_CHARACTERISTIC = '19b10002-e8f2-537e-4f6c-d104768a1214'
SENSOR_CHARACTERISTIC = '19b10001-e8f2-537e-4f6c-d104768a1214'

# Streamlit UI
st.title("ESP32 Bluetooth Control")
ble_state = st.empty()
retrieved_value = st.empty()
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

    # Get the services
    services = await ble_server.get_services()
    ble_service_found = False
    for service in services:
        if service.uuid == BLE_SERVICE:
            ble_service_found = True
            global SENSOR_CHARACTERISTIC, LED_CHARACTERISTIC
            SENSOR_CHARACTERISTIC = next(
                (char.uuid for char in service.characteristics if char.uuid == SENSOR_CHARACTERISTIC), None
            )
            LED_CHARACTERISTIC = next(
                (char.uuid for char in service.characteristics if char.uuid == LED_CHARACTERISTIC), None
            )
            break
    
    if not ble_service_found:
        ble_state.error("BLE Service not found")
        return

    if not SENSOR_CHARACTERISTIC or not LED_CHARACTERISTIC:
        ble_state.error("Required Characteristics not found")
        return

async def read_sensor_data():
    while True:
        if ble_server:
            try:
                value = await ble_server.read_gatt_char(SENSOR_CHARACTERISTIC)
                decoded_value = value.decode('utf-8')
                retrieved_value.write(f"Retrieved Value: {decoded_value}")
            except asyncio.CancelledError:
                retrieved_value.error("Read operation was cancelled.")
                break
            except Exception as e:
                retrieved_value.error(f"Error reading data: {e}")
        await asyncio.sleep(1)

async def control_led(state: bool):
    if ble_server:
        try:
            # Convert the boolean state to byte value (0 or 1)
            led_state = b'\x01' if state else b'\x00'
            await ble_server.write_gatt_char(LED_CHARACTERISTIC, led_state)
            st.write(f"LED {'on' if state else 'off'}")
        except Exception as e:
            st.error(f"Error controlling LED: {e}")

if st.button("Connect to ESP32"):
    try:
        asyncio.run(connect_to_device())
        if ble_server:
            asyncio.run(read_sensor_data())
    except Exception as e:
        st.error(f"An error occurred: {e}")

if st.button("Turn LED On"):
    asyncio.run(control_led(True))

if st.button("Turn LED Off"):
    asyncio.run(control_led(False))
