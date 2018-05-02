import config
from lora import LORA

from led import LED
from pytrack import Pytrack
from L76GNSS import L76GNSS # gps
#from LIS2HH12 import LIS2HH12 # acc
from time import sleep

def setup():

    LED.heartbeat(False)
    LED.off()

    global n, gps, sleep_time, dn, py

    # Initial sleep time
    sleep_time = 30

    # Connect to LoRaWAN Decent
    n = LORA()
    n.connect(config.dev_eui1416, config.app_eui, config.app_key1416)

    py = Pytrack()
    #print('{}V'.format(py.read_battery_voltage()))
    gps = L76GNSS(py, timeout=3)

    # Connect Sensors
    print("Setup... done")

if __name__ == "__main__":
    # Setup network & sensors

    setup()
    data = ""
    m_lat = m_lng = None
    # Measure
    try:
        #print ("Fetching gps position")
        m_lat, m_lng = gps.coordinates()
        battery = py.read_battery_voltage()
        battery = py.read_battery_voltage()
        print("Battery: ", battery)
        battery  = "%.2f" % float(battery) 
        temp = 20.5
        data = "%s %s %s %s" % (m_lat, m_lng, battery, temp)
        print("Data: ", data, "Size:", len(data))
    except Exception as e:
        print("Measure error: ", e)

    #print('Coords:', "{},{}".format(m_lat, m_lng))
    if m_lat == None: 
        print("Failed to receive gps signals")
        LED.blink(1, 0.1, 0x0000ff)
        LED.off()  
    else :
        # Send packet
        LED.blink(2, 0.1, 0xf0f000)
        LED.off()    

    response = n.send(data)

    #Go to deep sleep 
    py.setup_sleep(sleep_time)
    py.go_to_sleep()

