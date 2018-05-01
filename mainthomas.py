from startiot import Startiot
from L76GNSS import L76GNSS
from pytrack import Pytrack
import pycom
import time
from machine import Pin
from lib.onewire import DS18X20
from lib.onewire import OneWire
from lib.deepsleep import DeepSleep
pycom.heartbeat(False) # disable the blue blinking
iot = Startiot()


pycom.rgbled(0xFF0000)
iot.connect()
pycom.rgbled(0x0000FF)
pycom.rgbled(0x000000)

py = Pytrack()
l76 = L76GNSS(py, timeout=0)

# Temperature sensor 
ow = OneWire(Pin('P9'))
temp = DS18X20(ow)

ds = DeepSleep()

while True:
	
	# Get coordinates. Timeout in case of no coverage
	coord = l76.coordinates()

	# Get temperature
	tmp = temp.read_temp_async()
	temp.start_convertion()
	print(str(tmp))

	# send some coordinates
	pycom.rgbled(0x00FF00)
	#if not str(coord).split(", ")[0] == "(None" and not str(coord).split(", ")[1] == "None)":
	iot.send(str(coord) + " " + str(tmp)) 
	#	continue

	pycom.rgbled(0x000000)
	#iot.send(str(py.read_battery_voltage()) + " " + str(coord) + " " + str(tmp))
	py.go_to_sleep(2)
	print("Waking up...")