import logging
import random
import threading
import os
import sys
import ssl
from paho.mqtt import client as mqtt
from paho.mqtt.properties import Properties
from paho.mqtt.packettypes import PacketTypes
import time

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logging.getLogger("paho").setLevel(level=logging.DEBUG)
messages=[]

TOPIC = "test"
# PUB_TOPIC="house/sensor1"
# SUB_TOPIC = "test"


class CheckApp(object):
    """
    class to check some mqtt 5 functionality
    """

    def on_connect(self, client, userdata, flags, reasonCode, properties=None):
        """
        handler for connect
        """
        print('Connected with flags ', flags)
        print('Connected reason ', reasonCode)
        print('Connected properties', properties)
        print('Connected userdata', userdata)

    def on_message(self, client, userdata, message):
        """
        handler for message receive
        """
        msg = str(message.payload.decode("utf-8"))
        messages.append(msg)
        print('RECV Topic = ', message.topic)
        print('RECV MSG =', msg)

    def on_disconnect(self, client, userdata, flags, rc, properties=None):
        """
        handler for disconnect
        """
        print('Disconnected with flags ', flags)
        print('Disconnected reason ', rc)
        print('Disconnected properties ', properties)
        print('Disconnected userdata ', userdata)

    def on_subscribe(self, client, userdata, mid, granted_qos, properties=None):
        """
        handler for subscribe
        """
        print('SUBSCRIBED')

    def on_unsubscribe(self, client, userdata, mid, properties, reasonCodes):
        """
        handler for unsubscribe
        """
        print('UNSUBSCRIBED')

    def main(self):
        """
        main
        """
        port = 1883
        hostname = "localhost"

        print("creating 2 different clients for pub and sub with clean session=False and then subscribing")
        print("session will expire in 30 seconds")
        sub_client = mqtt.Client("subclient",protocol=mqtt.MQTTv5,transport="tcp",)
        pub_client = mqtt.Client("pubclient", protocol=mqtt.MQTTv5,transport="tcp",)
        sub_client.enable_logger(logging.getLogger("paho"))
        pub_client.enable_logger(logging.getLogger("paho"))

        sub_client.on_connect = self.on_connect
        pub_client.on_connect = self.on_connect
        sub_client.on_message = self.on_message
        sub_client.on_disconnect = self.on_disconnect
        sub_client.on_subscribe = self.on_subscribe

        connect_props = Properties(PacketTypes.CONNECT)
        print("Setting session expiry interval")
        properties.SessionExpiryInterval=30
        print("Subscribe client connecting for first time...")

        sub_client.connect(hostname, port, clean_start=False, properties=connect_props)
        sub_client.loop_start()

        print("Subscribe to topic at 1 qos")
        sub_client.subscribe(TOPIC, qos=1)

        time.sleep(5)
        print("Subscribe client disconnecting")
        sub_client.disconnect()
        sub_client.loop_stop()

        print("Publish client connecting and will publish while subscriber disconnected")
        # pub_client.connect(hostname, port, clean_start=False, properties=connect_props)
        pub_client.connect(hostname, port, properties=connect_props)
        # pub_client.connect(host)

        msg_out1="Testing session expire interval- part1"
        print("Publishing messages while disconnected")
        publish_properties = Properties(PacketTypes.PUBLISH)
        pub_client.publish('test', msg_out1, qos=1, properties=publish_properties)
        print("waiting 20 seconds= ")
        time.sleep(20)
        
        print("Subscriber connecting expect to receive message")
        sub_client.connect(host,clean_start=False,properties=properties)
        sub_client.loop_start()
        #sub_client.subscribe('test', qos=1)
        time.sleep(5) #wait to receive message
        if len(messages)==0:
            print("test failed")
        else:
            msg=messages.pop()
            if msg==msg_out1:
                print("test succeeded")

        ###Part 2

        properties=Properties(PacketTypes.CONNECT)
        print("Setting session expiry interval")
        properties.SessionExpiryInterval=30 #set session expiry interval
        sub_client.connect(host,clean_start=False,properties=properties)
        sub_client.loop_start()
        sub_client.subscribe(TOPIC,qos=1)

        time.sleep(5)
        print("Subscribe client disconnecting")
        sub_client.disconnect()
        sub_client.loop_stop()
        print("Publish client Connecting and will publish while receiver disconnected")

        # pub_client.connect(hostname, port, clean_start=False, properties=connect_props)
        pub_client.connect(hostname, port, properties=connect_props)
        msg_out1="Testing session expire interval- part2"
        print("Publishing messages while disconnected")
        pub_client.publish('test', msg_out1,qos=1)
        print("Waiting 40 seconds= ")
        time.sleep(40)
        print("Connecting don't expect to receive messages as session should have expired")

        sub_client.connect(host,clean_start=False,properties=properties)

        sub_client.loop_start()

        time.sleep(5) #wait to receive message
        if len(messages)==0:
            print("test succeeded")
        else:
            msg=messages.pop()
            if msg==msg_out1:
                print("test failed")
        sub_client.loop_stop()
        sub_client.disconnect()
        pub_client.disconnect()


if __name__ == "__main__":
    CheckApp().main()