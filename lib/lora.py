import socket
from binascii import unhexlify
from network import LoRa
from led import LED
import pycom 

class LORA(object):
    'Wrapper class for LoRa'

    # LoRa and socket instances
    lora = None
    s = None

    def connect(self, dev_eui, app_eui, app_key):
        """
        Connect device to LoRa.
        Set the socket and lora instances.
        """
        
        dev_eui = unhexlify(dev_eui)
        app_eui = unhexlify(app_eui)
        app_key = unhexlify(app_key)
        
        # Disable blue blinking and turn LED off
        LED.heartbeat(False)
        LED.off()

        # Initialize LoRa in LORAWAN mode
        self.lora = LoRa(mode = LoRa.LORAWAN)

        #Check if lora connection is saved because of deep sleep
        loraSaved = pycom.nvs_get('loraSaved')
        if (not loraSaved):
            print("Lora not saved")
            # Join a network using OTAA (Over the Air Activation)
            self.lora.join(activation = LoRa.OTAA, auth = (dev_eui, app_eui, app_key), timeout = 0)
            # Wait until the module has joined the network
            count = 0
            while not self.lora.has_joined():
                LED.blink(1, 2.5, 0xff0000)
                print("Trying to join: " ,  count)
                count = count + 1
                if (count > 50):
                    return False
        
            LED.blink(2, 0.1)
            LED.off()
            pycom.nvs_set('loraSaved', 1)
        else:
            print("Lora was saved")
            self.lora.nvram_restore()
            LED.blink(2, 0.1, 0x0f0f0f)
            LED.off()
        
        self.lora.nvram_save()

        # Create a LoRa socket
        self.s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

        # Set the LoRaWAN data rate
        self.s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

        # Make the socket non-blocking
        self.s.setblocking(True)

        # print ("Joined! ",  count)
        # print("Create LoRaWAN socket")

        # Create a raw LoRa socket
        self.s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
        self.s.setblocking(True)
        return True 
        
    def send(self, data):
        """
        Send data over the network.
        """
        tries = 0 
        while tries < 5: 
            try:
                self.s.send(data)
                LED.blink(2, 0.1, 0x00ff00)
                print("Sending data:")
                print(data)
                tries = 5
            except OSError as e:
                LED.blink(2, 0.2, 0xff0000)
                print ("Failed to send data")
                if e.errno == 11:
                    print("Caught exception while sending")
                    print("errno: ", e.errno)
                tries += 1
                if (tries == 5):
                    pycom.nvs_erase('loraSaved')
            
        LED.off()
        #data = self.s.recv(64)
        #print("Received data:", data)

        return " "#data

    # Erease state telling that lora is saved. Will initate new connection next time. 
    def ereaseloraSaved(self):
        pycompycom.nvs_erase('loraSaved')