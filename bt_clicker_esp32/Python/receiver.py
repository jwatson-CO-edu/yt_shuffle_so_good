# Source: https://claude.ai/share/99f4f95b-8539-48d7-9684-fdddfc04d2c5
# python3.11 -m pip install selenium --user

########## INIT ####################################################################################
import simplepyble
import pynput
from pynput.mouse import Button
from pynput.keyboard import Key
from time import sleep
import numpy as np
from PIL import ImageGrab
from pprint import pformat

# UUID for the service and characteristic that send our signal
# These should match the UUIDs in your ESP32 code
SERVICE_UUID        = "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
CHARACTERISTIC_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"
_START_LOC          = [ 592,  732 ] # Image Space
_AD_OFFSET          = [ -80-10, -120-10 ] # Mouse Space


########## SCREEN IMAGE ANALYSIS ###################################################################

def get_image():
    printscreen_pil   = ImageGrab.grab( all_screens = True )
    # printscreen_pil.show()
    printscreen_numpy = np.array( printscreen_pil.getdata(), dtype='uint8' ).reshape(
        (printscreen_pil.size[1], printscreen_pil.size[0], 3,)
    )
    return printscreen_numpy


def get_swatch_avg_value( img : np.ndarray, x0y0, x1y1 ):
    swatch = img[ x0y0[0]:x1y1[0], x0y0[1]:x1y1[1], : ]
    rtnVal = np.sum( swatch ) / swatch.size
    # print( rtnVal )
    return rtnVal


def get_video_bbox( img, startLoc, swatchWidth = 40, swatchThick = 4, thresh = 255*0.95 ):
    """ Attempt to find the edges of the video """
    hWidth = int( swatchWidth / 2 )
    incr   = 1 #swatchThick
    xBox   = [[startLoc[0], startLoc[1]-hWidth], [startLoc[0]+swatchThick, startLoc[1]+hWidth,],]
    yBox   = [[startLoc[0]-hWidth, startLoc[1],], [startLoc[0]+hWidth, startLoc[1]+swatchThick,],]
    vals   = [0.0, 0.0,]
    corner = startLoc
    while vals[0] < thresh:
        vals[0] = get_swatch_avg_value( img, xBox[0], xBox[1] )
        if vals[0] >= thresh:
            corner[0] = xBox[1][0]
        else:
            xBox[0][0] += incr
            xBox[1][0] += incr
    while vals[1] < thresh:
        vals[1] = get_swatch_avg_value( img, yBox[0], yBox[1] )
        if vals[1] >= thresh:
            corner[1] = yBox[1][1]
        else:
            yBox[0][1] += incr
            yBox[1][1] += incr
    return corner


def get_yt_bbox():
    """ Get the bounding box of the YT video """
    img  = get_image()
    crnr = get_video_bbox( img, _START_LOC, swatchWidth = 40, swatchThick = 4, thresh = 255*0.95 )
    return [crnr[1], crnr[0]] # Image space to mouse space



########## MAIN ####################################################################################
def main():
    # Initialize controller
    mouse    = pynput.mouse.Controller()
    keyboard = pynput.keyboard.Controller()
    
    # Initialize SimplePyBLE
    adapter  = None
    adapters = simplepyble.Adapter.get_adapters()
    
    if not adapters:
        print( "No Bluetooth adapters found." )
        return
    
    # Select adapter (usually there's only one)
    adapter = adapters[1]
    print( f"Using adapter: {adapter.identifier()}" )
    
    # Start scanning
    print( "Scanning for devices..." )
    adapter.scan_for( 15000 )  # Scan for 5 seconds
    
    # Get discovered devices
    devices = adapter.scan_get_results()
    if not devices:
        print( "No devices found." )
        return
    
    # Display and select device
    print( "Found devices:" )
    selection = -1
    for i, device in enumerate( devices ):
        print( f"{i}: {device.identifier()} - {device.address()}" )
        if "ESP32-C3 Mouse Control" in device.identifier():
            selection = i
            print( f"SELECTED {i}!" )
            break
    if selection < 0:
        raise RuntimeError( f"Could NOT find the expected device among:\n{pformat( devices, indent = 2 )}" )
    
    # Select device
    if len(devices) == 1:
        selected_device = devices[0]
    else:
        selected_device = devices[ selection ]
    
    print(f"Connecting to {selected_device.identifier()} ({selected_device.address()})...")
    
    # Connect to device
    selected_device.connect()
    print( "Connected!" )
    
    # Get services and characteristics
    services              = selected_device.services()
    target_service        = None
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
        print( f"Could not find characteristic {CHARACTERISTIC_UUID}" )
        selected_device.disconnect()
        return
    
    def short_kb_press( k, s ):
        """ Press `k` for `s` """
        if isinstance( k, list ):
            for key in k:
                keyboard.press( key )
            sleep( s )
            for key in k:
                keyboard.release( key )
        else:
            keyboard.press( k )
            sleep( s )
            keyboard.release( k )
    
    _PRESS_TIME_S = 0.05

    # Set up notification callback
    def notification_callback( data ):
        try:
            signal = bytes( data ).decode( 'utf-8' ).strip()
            print( f"Received: {signal}, The current mouse position is: {mouse.position}" )
            # https://nitratine.net/blog/post/simulate-keypresses-in-python/#pressing-and-releasing-keys

            if signal == "CLICK":
                corner = get_yt_bbox()
                nuPosn = [int(item) for item in np.add( corner, _AD_OFFSET ).tolist()]
                print( f"Sending mouse to: {nuPosn}" )
                mouse.position = nuPosn
                mouse.click( Button.left )

            elif signal == "FWD":
                print( "Performing right arrow" )
                short_kb_press( Key.right, _PRESS_TIME_S )
            elif signal == "BCK":
                print( "Performing left arrow" )
                short_kb_press( Key.left, _PRESS_TIME_S )
            elif signal == "NEXT":
                print( "Performing [Shift]+[n]" )
                short_kb_press( [Key.shift, 'n'], _PRESS_TIME_S )
            elif signal == "VOLUP":
                print( "Performing Volume Up" )
                short_kb_press( Key.media_volume_up, _PRESS_TIME_S )
            elif signal == "VOLDN":
                print( "Performing Volume Down" )
                short_kb_press( Key.media_volume_down, _PRESS_TIME_S )

            # FIXME: ADD SPOTIFY FUNCTIONS!
            # https://support.spotify.com/de-en/article/keyboard-shortcuts/
            # https://spotipy.readthedocs.io/en/2.25.1/index.html#spotipy.client.Spotify.start_playback
            
        except Exception as e:
            print( f"Error processing notification: {e}" )
    
    # Subscribe to notifications
    selected_device.notify( target_service.uuid(), target_characteristic.uuid(), notification_callback )
    
    print( "Listening for signals. Press Ctrl+C to exit..." )
    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        selected_device.disconnect()
        print( "Disconnected" )

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt as e:
        print( f"Session ENDED by user!\n{e}\n" )
        exit(0)
    except RuntimeError as e:
        print( f"Session ENDED by script!\n{e}\n" )
        exit(1)