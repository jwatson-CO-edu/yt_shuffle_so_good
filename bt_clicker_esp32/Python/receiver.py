# https://claude.ai/share/99f4f95b-8539-48d7-9684-fdddfc04d2c5
import time
import sys
import PyBluez as bluetooth
from pynput.mouse import Button, Controller

def main():
    # Initialize mouse controller
    mouse = Controller()
    
    # Initialize Bluetooth
    print("Initializing Bluetooth...")
    nearby_devices = bluetooth.discover_devices(lookup_names=True)
    print(f"Found {len(nearby_devices)} devices.")
    
    # Display all found devices
    for addr, name in nearby_devices:
        print(f"Device: {name} - Address: {addr}")
    
    # Ask for device selection if multiple devices found
    if len(nearby_devices) > 0:
        if len(nearby_devices) == 1:
            # Auto-select if only one device found
            target_addr = nearby_devices[0][0]
            target_name = nearby_devices[0][1]
        else:
            # Let user choose
            selection = int(input("Select device number (0-" + str(len(nearby_devices)-1) + "): "))
            target_addr = nearby_devices[selection][0]
            target_name = nearby_devices[selection][1]
            
        print(f"Connecting to {target_name} ({target_addr})...")
        
        # Set up socket
        sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        port = 1  # Most devices use port 1 for RFCOMM communication
        
        try:
            # Connect to device
            sock.connect((target_addr, port))
            print("Connected! Waiting for signals...")
            
            # Main loop for receiving signals
            while True:
                try:
                    data = sock.recv(1024)
                    if not data:
                        continue
                    
                    # Assuming the device sends a specific signal like "CLICK"
                    # Modify this as needed for your specific device
                    if data.decode('utf-8').strip() == "CLICK":
                        print("Signal received, performing mouse click")
                        mouse.click(Button.left)
                        
                except bluetooth.btcommon.BluetoothError as e:
                    print(f"Bluetooth Error: {e}")
                    break
                    
                except KeyboardInterrupt:
                    print("Program terminated by user")
                    break
                    
        except Exception as e:
            print(f"Error: {e}")
            
        finally:
            # Clean up connection
            sock.close()
            print("Bluetooth connection closed")
    else:
        print("No Bluetooth devices found. Make sure your device is discoverable.")

if __name__ == "__main__":
    main()
