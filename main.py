import config
from lora import LORA

from led import LED
from pytrack import Pytrack
from L76GNSS import L76GNSS # gps
from LIS2HH12 import LIS2HH12 # acc
from time import sleep
import uos

def setup():

    LED.heartbeat(False)
    LED.off()

    global n, gps, sleep_time, dn, py, acc

    # Initial sleep time
    sleep_time = 60 * 3
    py = Pytrack()


    # Connect to LoRaWAN Decent
    n = LORA()
    if (not n.connect(config.dev_eui1416, config.app_eui, config.app_key1416)): 
        # If still not connected, go to sleep one minute and try again (reboots after sleep).
        py.setup_sleep(60)
        py.go_to_sleep(gps=True)

    
    gps = L76GNSS(py, timeout=30)

    acc = LIS2HH12(py)
    # Connect Sensors
    print("Setup... done")

if __name__ == "__main__":
    # Setup network & sensors

    setup()
    data = ""
    m_lat = m_lng = None
    # Measure
    try:
        # Don't hava an temperature sensor, so just sets an value 
        temp =  uos.urandom(1)[0]/256*7 + 8
        print("Temp: ", temp)
        sleep(1)
        m_lat, m_lng = gps.coordinates()
        print ("GPS: %s, %s " % (m_lat, m_lng))
        sleep(1)
        x, y, z = acc.acceleration()
        print ("Acc: x: %s, y: %s, z: %s" % (x, y, z))
        x_1, y_1, z_1 = "%.2f" % x, "%.2f" % y, "%.2f" % z 
        sumAcc = "%.2f" % (float(x_1) + float(y_1) + float(z_1))
        print ("Sum x, y, z Acc: %s" % (sumAcc))

        battery = py.read_battery_voltage()
        battery = py.read_battery_voltage()
        print("Battery: ", battery)
        battery  = "%.2f" % float(battery) 
        
        
        data = "%s %s %s %s %s" % (m_lat, m_lng, battery, temp, sumAcc)
        print("Data: ", data, "Size:", len(data))
    except Exception as e:
        print("Measure error: ", e)

    #print('Coords:', "{},{}".format(m_lat, m_lng))
    if m_lat == None: 
        print("Failed to receive gps signals")
        LED.blink(1, 0.1, 0x0000ff)
        LED.off()  
    else :
        # Send packe
        LED.blink(2, 0.1, 0xf0f000)
        LED.off()    
    try:
        response = n.send(data)
    except:
        print("Failed to send data, should try to reconnect")
        n.eraseloraSaved()


    #Go to deep sleep 
    py.setup_sleep(sleep_time)
    py.go_to_sleep(gps=True)

