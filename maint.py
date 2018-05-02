from config import dev_eui, app_eui, app_key, dev_eui2, app_key2
from lora import LORA

from led import LED
from pytrack import Pytrack
from L76GNSS import L76GNSS # gps
#from LIS2HH12 import LIS2HH12 # acc

from time import sleep
from machine import Pin
from lib.onewire import DS18X20
from lib.onewire import OneWire
from lib.deepsleep import DeepSleep
import sys

setupDone = False

def setup():
    global n, gps, sleep_time, dn, py, temp, n2, setupDone
    setupDone = True
    # Initial sleep time
    sleep_time = 10

    # Connect to LoRaWAN Decent
    n = LORA()
    try:
        loraSaved = pycom.nvs_get('loraSaved')
        print ("LoraSaved: ", loraSaved)
        if (not loraSaved):
            print("Lora not saved")
            n.connect(dev_eui2, app_eui, app_key2)
            pycom.nvs_set('loraSaved', 1)
        else:
            print("Lora was saved")
            n.connect(dev_eui2, app_eui, app_key2, True)
    except:
        print("Lora not saved, exception")
        n.connect(dev_eui2, app_eui, app_key2)
        pycom.nvs_set('loraSaved', 1)


    py = Pytrack()
    #print('{}V'.format(py.read_battery_voltage()))
    gps = L76GNSS(py, timeout=10)

    # Connect Sensors
    ow = OneWire(Pin('P9'))
    temp = DS18X20(ow)

    print("Setup... done")


if __name__ == "__main__":
    # Setup network & sensors
    LED.heartbeat(False)
    LED.off()
    while True:
        setup()
        sleep(sleep_time)
        data = ""
        m_lat = m_lng = None
        # Measure
        try:
            print ("Fetching gps position")
            #m_lat, m_lng = gps.coordinates()
            battery = py.read_battery_voltage()
            print("Battery: ", battery)
            battery  = "%.2f" % float(battery) 
            tmp = 100.0
            count = 0 
            # Get temperature
            while (float(tmp) > 50.0 and count < 10):
                tmp = temp.read_temp_async()
                temp.start_convertion()
                tmp  = "%.2f" % float(tmp) 
                print(tmp, "Tries: ", count)
                count += 1  

            data = "%s %s %s %s" % (m_lat, m_lng, str(battery), str(tmp))
            print("Data: ", data, "Size: ", len(data))
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
        
        #response = n.send(data)


        # py.setup_sleep(sleep_time)
        # print("Goes to sleep: ", sleep_time, "s")
        # py.go_to_sleep()
