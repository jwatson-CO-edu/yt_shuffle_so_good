import numpy as np
from PIL import ImageGrab
import pynput 

_START_LOC = [ 592,  732 ] # Image Space
_AD_OFFSET = [ -80, -120 ] # Mouse Space


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
    crnr = get_video_bbox( img, _START_LOC, swatchWidth = 40, swatchThick = 4, thresh = 255*0.999 )
    return [crnr[1], crnr[0]]



if __name__ == "__main__":
    mouse  = pynput.mouse.Controller()
    corner = get_yt_bbox()
    mPosn  = mouse.position
    print( f"Mouse: {mPosn}" )
    print( f"Corner: {corner}" )
    print( f"Offset: {np.subtract( mPosn, corner)}" )
