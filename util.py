import paho.mqtt.client as mqtt
import time


class MQTTMessageReceiver:
    def __init__(self, broker_address, topic):
        self.broker_address = broker_address
        self.topic = topic
        self.message = None
        self.client = mqtt.Client()
        self.client.on_message = self.on_message

    def on_message(self, client, userdata, message):
        self.message = message.payload.decode("utf-8")

    def wait_for_message(self):
        self.client.connect(self.broker_address)
        self.client.subscribe(self.topic)
        self.client.loop_start()

        while self.message is None:
            time.sleep(0.1)

        self.client.loop_stop()
        self.client.disconnect()
        return self.message




# Example usage
if __name__ == "__main__":
    '''broker_address = "mqtt.eclipse.org"  # Change this to your MQTT broker's address
    topic = "your_topic"  # Change this to the desired MQTT topic

    mqtt_receiver = MQTTMessageReceiver("192.168.225.13", "authentic")
    received_message = mqtt_receiver.wait_for_message()

    print("Received Message:", received_message)'''

