from config import dev_eui, app_eui, app_key, dev_eui2, app_key2
from lora import LORA

from led import LED
from pytrack import Pytrack
from L76GNSS import L76GNSS # gps
#from LIS2HH12 import LIS2HH12 # acc

from time import sleep

def setup():
    global n, gps, sleep_time, dn, py
    
    # Initial sleep time
    sleep_time = 15

    # Connect to LoRaWAN Decent
    n = LORA()
    n.connect(dev_eui, app_eui, app_key)

    py = Pytrack()
    #print('{}V'.format(py.read_battery_voltage()))
    gps = L76GNSS(py, timeout=10)

    # Connect Sensors
    print("Setup... done")


if __name__ == "__main__":
    # Setup network & sensors
    setup()

    while True:
        #sleep(sleep_time)
        #py.setup_sleep(60)
        #py.go_to_sleep()
        data = ""
        m_lat = m_lng = None
        # Measure
        try:
            print ("Fetching gps position")
            m_lat, m_lng = gps.coordinates()
            battery = '{}V'.format(py.read_battery_voltage())

            data = "%s %s %s" % (m_lat, m_lng, battery)
            #print("Data: ", data)
        except Exception as e:
            print("Measure error: ", e)

        #print('Coords:', "{},{}".format(m_lat, m_lng))
        if m_lat == None: 
            print("Failed to receive gps signals")
            LED.blink(2, 0.1, 0x0000ff)  
        else :
            # Send packet
            LED.blink(2, 0.1, 0xf0f000)        
            response = n.send(data)


