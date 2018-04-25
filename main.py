from config import dev_eui, app_eui, app_key, dummyThings
from lora import LORA

from led import LED
from pytrack import Pytrack
from L76GNSS import L76GNSS # gps
#from LIS2HH12 import LIS2HH12 # acc

from time import sleep

def setup():
    global n, gps, sleep_time, dn
    
    # Initial sleep time
    sleep_time = 30

    # Connect to LoRaWAN Decent
    n = LORA()
    n.connect(dev_eui, app_eui, app_key)
    

    py = Pytrack()
    gps = L76GNSS(py)

    # Connect Sensors
    print("Setup... done")


if __name__ == "__main__":
    # Setup network & sensors
    setup()
    #LED.heartbeat(False)
    #LED.off()

    while True:
        sleep(sleep_time)

        data = ""
        m_lat = m_lng = None
        # Measure
        try:
            print ("Fetching gps position")
            #m_lat, m_lng = gps.coordinates()
            m_lat, m_lng = (69.691775, 18.963121)

            data = "%s %s %s" % (m_lat, m_lng, "GGgpssignal")
        except Exception as e:
            print("Measure error: ", e)

        print('Coords:', "{},{}".format(m_lat, m_lng))
        if m_lat == None: 
            data = "%s %s %s" % (m_lat, m_lng, "NoGpsSignal")
            LED.blink(2, 0.1, 0x0000ff)  
        else :
            # Send packet
            LED.blink(2, 0.1, 0xf0f000)        

        response = n.send(data)


