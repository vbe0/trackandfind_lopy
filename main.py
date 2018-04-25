from config import dev_eui, app_eui, app_key
from lora import LORA

from led import LED
from pytrack import Pytrack
from L76GNSS import L76GNSS # gps
#from LIS2HH12 import LIS2HH12 # acc

from time import sleep

def setup():
    global n, gps, sleep_time
    
    # Initial sleep time
    sleep_time = 3

    # Connect to LoRaWAN
    n = LORA()
    n.connect(dev_eui, app_eui, app_key)
    
    py = Pytrack()
    gps = L76GNSS(py)

    # Connect Sensors
    print("Setup... done")

if __name__ == "__main__":
    # Setup network & sensors
    LED.heartbeat(False)
    LED.off()
    setup()

    while True:
        sleep(sleep_time)

        data = ""
        m_lat = m_lng = None
        # Measure
        try:
            m_lat, m_lng = gps.coordinates()
            #print('Coords:', "{},{}".format(m_lat, m_lng))

            data = "%s %s %s" % (m_lat, m_lng, "GG gps signal")
        except Exception as e:
            print("Measure error: ", e)

        if m_lat == None: 
            data = "%s %s %s" % (m_lat, m_lng, "No Gps Signal")
            LED.blink(2, 0.5, 0x0000ff)  
        else :
            # Send packet
            LED.blink(2, 2.5, 0x00fff0)        
            response = n.send(data)


