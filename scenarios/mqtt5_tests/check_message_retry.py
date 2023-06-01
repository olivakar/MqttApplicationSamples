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

TOPIC = "samples/telemetry"
connected_event = threading.Event()


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
        # connected_event.set()
        # subscribe to same topic
        print("Subscribing")
        client.subscribe(TOPIC)

    def on_message(self, client, userdata, message):
        """
        handler for message receive
        """
        msg = str(message.payload.decode("utf-8"))
        print('RECV Topic = ', message.topic)
        print('RECV MSG =', msg)

    def on_disconnect(self, client, userdata, rc, properties=None):
        """
        handler for disconnect
        """
        print('Disconnected reason ', rc)
        print('Disconnected properties ', properties)
        print('Disconnected userdata ', userdata)
        # connected_event.clear()

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

    def send_publish(self, mqtt_client, i, qos):
        """
        publish
        """
        publish_properties = Properties(PacketTypes.PUBLISH)
        msg = "hello world {}".format(i)
        print("Sending publish id {}".format(i))
        mqtt_client.publish(TOPIC, msg, qos=qos, properties=publish_properties)
        #  mi.wait_for_publish()

    def main(self):
        """
        main
        """
        port = 1883
        hostname = "127.0.0.1"
        client_id = "harry_potter"

        mqtt_client = mqtt.Client(
            client_id=client_id,
            protocol=mqtt.MQTTv5,
            transport="tcp",
        )
        mqtt_client.enable_logger(logging.getLogger("paho"))
        # mqtt_client.username_pw_set("someusername", "somepassword")
        # ssl_context = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS_CLIENT)
        # ssl_context.verify_mode = ssl.CERT_REQUIRED
        # with open("chain.pem", mode="r") as ca_cert_file:
        #   server_verification_cert = ca_cert_file.read()
        # ssl_context.load_verify_locations(cadata=server_verification_cert)
        # # ssl_context.load_default_certs()
        
        # ssl_context.load_cert_chain(certfile="sample_client.pem", keyfile="sample_client.key", password="mqtt")
        
        # ssl_context.check_hostname = True
        # mqtt_client.tls_set_context(ssl_context)

        mqtt_client.on_connect = self.on_connect
        mqtt_client.on_message = self.on_message
        mqtt_client.on_disconnect = self.on_disconnect
        mqtt_client.on_subscribe = self.on_subscribe

        connect_props = Properties(PacketTypes.CONNECT)
        print("Connecting for first time...")

        mqtt_client.connect(hostname, port, clean_start=False, properties=connect_props)
        mqtt_client.loop_start()

        # Publish at qos=1
        self.send_publish(mqtt_client, 1, qos=1)
        self.send_publish(mqtt_client, 2, qos=1)
        self.send_publish(mqtt_client, 3, qos=1)

        # Simulate a network failure by disconnecting from the broker
        mqtt_client.disconnect()
        mqtt_client.loop_stop()

        # Wait for a while to simulate the network downtime
        print("sleep for random time to have downtime")
        time.sleep(random.randint(5,8))

        print("Connecting again...")
        mqtt_client.connect(hostname, port, clean_start=False, properties=connect_props)
        mqtt_client.loop_start()


if __name__ == "__main__":
    CheckApp().main()