import time
import sys
from umqtt.simple import MQTTClient
import ubinascii
import machine
import micropython
import esp
import random
esp.osdebug(None)
import temperature
import gc
gc.collect()


#MQTT
mqtt_server = "io.adafruit.com"
client_id = ubinascii.hexlify(machine.unique_id())
topic_pub = b"TestValue"


def mqtt():
    c = MQTTClient(
        client_id='esp32',
        user = 'esp32',
        server = '178.197.211.141',
        password='Jsf87648',
        port=1883
    )
    c.connect()
    c.publish('Jeppy/feeds/Test', b'{}'.format(_))
    c.disconnect()

def main():
    print(temperature.get_temperature())

if __name__ == "__main__":
    main()