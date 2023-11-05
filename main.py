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

#Config_File
config_file = json.load(open('config.json'))

#MQTT
mqtt_server = config_file['mqtt']['server']
client_id = ubinascii.hexlify(machine.unique_id())
topic_pub = b"TestValue"


def mqtt(data):
    c = MQTTClient(
        client_id = config_file['mqtt']['client_id'],
        #user = 'config_file['mqtt']['user'],
        server = config_file['mqtt']['server'],
        #password = 'aio_hmHz68Df4iapfQ67MxctYnMLaihZ'
    )
    c.connect()
    c.publish(config_file['mqtt']['topic'], b'{}'.format(data))
    c.disconnect()

def main():
    while True:
        time.sleep(1)
        temperature_value = temperature.get_celcius(random.randint(28000,35000))
        print(temperature_value)
        mqtt(temperature_value)

if __name__ == "__main__":
    main()


