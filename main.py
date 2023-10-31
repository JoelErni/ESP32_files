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
        user = 'Jeppy',
        server = mqtt_server,
        password = 'aio_raiJ46lNLXapjuFVKxnSv7SzeCi8'
    )
    c.connect()
    c.publish('Jeppy/feeds/test', b'{}'.format(data))
    c.disconnect()

def main():
    temperature = temperature.get_celcius(random.randint(28000,35000))
    print(temperature)
    mqtt(temperature)

if __name__ == "__main__":
    main()