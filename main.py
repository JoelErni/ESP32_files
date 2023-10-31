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


def mqtt(data):
    c = MQTTClient(
        client_id='0',
        #user = 'Jeppy',
        server = "185.80.65.82:1883",
        #password = 'aio_hmHz68Df4iapfQ67MxctYnMLaihZ'
    )
    c.connect()
    c.publish('hello/topic', b'{}'.format(data))
    c.disconnect()

def main():
    temperature_value = temperature.get_celcius(random.randint(28000,35000))
    print(temperature_value)
    mqtt(temperature_value)

if __name__ == "__main__":
    main()

