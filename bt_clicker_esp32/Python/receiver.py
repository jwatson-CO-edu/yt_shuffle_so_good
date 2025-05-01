# https://claude.ai/share/99f4f95b-8539-48d7-9684-fdddfc04d2c5
import simplepyble
from pynput.mouse import Button, Controller
import time

import simplepyble._simplepyble

# UUID for the service and characteristic that send our signal
# These should match the UUIDs in your ESP32 code
SERVICE_UUID = "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
CHARACTERISTIC_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"

def main():
    # Initialize mouse controller
    mouse = Controller()
    
    # Initialize SimplePyBLE
    adapter = None
    adapters = simplepyble.Adapter.get_adapters()
    
    if not adapters:
        print("No Bluetooth adapters found.")
        return
    
    # Select adapter (usually there's only one)
    adapter = adapters[1]
    print(f"Using adapter: {adapter.identifier()}")
    
    # Start scanning
    print("Scanning for devices...")
    adapter.scan_for( 15000 )  # Scan for 5 seconds
    
    # Get discovered devices
    devices = adapter.scan_get_results()
    if not devices:
        print("No devices found.")
        return
    
    # Display and select device
    print("Found devices:")
    selection = 0
    for i, device in enumerate(devices):
        print(f"{i}: {device.identifier()} - {device.address()}")
        if "ESP32-C3 Mouse Control" in device.identifier():
            selection = i
            print(f"SELECTED {i}!")
            break
    
    # Select device
    if len(devices) == 1:
        selected_device = devices[0]
    else:
        selected_device = devices[ selection ]
    
    print(f"Connecting to {selected_device.identifier()} ({selected_device.address()})...")
    
    # Connect to device
    selected_device.connect()
    print("Connected!")
    
    # Get services and characteristics
    services = selected_device.services()
    target_service = None
    target_characteristic = None
    
    # Find our service and characteristic
    for service in services:
        if service.uuid() == SERVICE_UUID:
            target_service = service
            for characteristic in service.characteristics():
                if characteristic.uuid() == CHARACTERISTIC_UUID:
                    target_characteristic = characteristic
                    break
            break
    
    if not target_characteristic:
        print(f"Could not find characteristic {CHARACTERISTIC_UUID}")
        selected_device.disconnect()
        return
    
    # Set up notification callback
    def notification_callback(data):
        try:
            signal = bytes(data).decode('utf-8').strip()
            print(f"Received: {signal}")
            if signal == "CLICK":
                print("Performing mouse click")
                mouse.click(Button.left)
        except Exception as e:
            print(f"Error processing notification: {e}")
    
    # Subscribe to notifications
    selected_device.notify(target_service.uuid(), target_characteristic.uuid(), notification_callback)
    
    print("Listening for signals. Press Ctrl+C to exit...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        selected_device.disconnect()
        print("Disconnected")

if __name__ == "__main__":
    main()