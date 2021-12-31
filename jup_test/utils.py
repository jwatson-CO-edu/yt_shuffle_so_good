import time 
from time import sleep


class Heartbeat:
    """ Maintain a frequency no greater than that specified """
    
    def __init__( self, freqHz ):
        """ Setup the specified frequency and init timer """
        self.freqHz = freqHz
        self.period = 1.0/freqHz
        self.last   = time.time()
        
    def rest( self ):
        """ Rest for an interval that does not allow the frequency to be exceeded """
        nowTime = time.time()
        timeDif = self.period - (nowTime - self.last)
        if timeDif > 0:
            sleep( timeDif )
        self.last = nowTime