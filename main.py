from config import dev_eui, app_eui, app_key, dev_eui2, app_key2
from lora import LORA

from led import LED
from pytrack import Pytrack
from L76GNSS import L76GNSS # gps
#from LIS2HH12 import LIS2HH12 # acc

from time import sleep

def setup():
    global n, gps, sleep_time, dn, py, is_n
    
    is_n = True
    # Initial sleep time
    sleep_time = 15

    # Connect to LoRaWAN Decent
    n = LORA()
    n.connect(dev_eui, app_eui, app_key)

    n2 = LORA()
    n.connect(dev_eui2, app_eui, app_key2)
    

    py = Pytrack()
    #print('{}V'.format(py.read_battery_voltage()))
    gps = L76GNSS(py, timeout=10)

    # Connect Sensors
    print("Setup... done")

def sendData(m_lat, m_lng, battery): 
    global is_n
    if (is_n):
        data = "%s %s %s" % (m_lat, m_lng, battery)
        n.send(data)
        is_n = False
    else:
        lat = m_lat - 69.737993 + m_lat
        lng = m_lng - 18.812860 + m_lat
        data = "%s %s %s" % (lat, lng, battery)
        n2.send(data)
        is_n = True

if __name__ == "__main__":
    # Setup network & sensors
    setup()

    while True:
        sleep(sleep_time)

        data = ""
        m_lat = m_lng = None
        # Measure
        try:
            print ("Fetching gps position")
            m_lat, m_lng = gps.coordinates()
            battery = '{}V'.format(py.read_battery_voltage())

            #data = "%s %s %s" % (m_lat, m_lng, battery)
            #print("Data: ", data)
        except Exception as e:
            print("Measure error: ", e)

        #print('Coords:', "{},{}".format(m_lat, m_lng))
        if m_lat == None: 
            LED.blink(2, 0.1, 0x0000ff)  
        else :
            # Send packet
            LED.blink(2, 0.1, 0xf0f000)        
            #response = n.send(data)
            sendData(m_lat, m_lng, battery)


