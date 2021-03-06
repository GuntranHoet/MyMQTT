import time
import paho.mqtt.client as mqtt # 1.5.1

# Useful source with simple MQTT explenations:
# http://www.steves-internet-guide.com/mqtt-basics-course/
# Retained messages:
# http://www.steves-internet-guide.com/mqtt-retained-messages-example/
# Last will messages:
# http://www.steves-internet-guide.com/mqtt-last-will-example/

class MyMQTT:
    def __init__(self, clientName, host, user, password, qos = 0):
        # define variables
        self.host = host
        self.user = user
        self.password = password
        self.qos = qos
        self.clientName = clientName
        self.client = None
        self.printPrefix = f"MQTT::{self.clientName}:"
        self.keepAlive = 60 # 60 is MQTT default
        # setup client
        self.client = mqtt.Client( self.clientName )
        self.client.username_pw_set( self.user, self.password )
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_log = self.on_log
        self.client.on_publish = self.on_publish

    ###############################################################

    ## optional setup functions ##
    
    def setup_setLastWill(self, topic, data, retain=True):
        # we want to be sure this arrives
        qos = self.qos if ( self.qos > 0 ) else 1
        self.client.will_set(topic, data, qos, retain)
        print(self.printPrefix + ":will_set:", f"set to '{topic}' = '{data}'")
    
    def setup_setKeepAlive(self, keepAlive = 60):#
        # 60 is MQTT default
        self.keepAlive = keepAlive
        print(self.printPrefix + ":keepAlive:", f"set to '{keepAlive}'")

    ###############################################################

    ## callbacks ##

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print(self.printPrefix + ":on_connect:", "Connected OK")
        else:
            print(self.printPrefix + ":on_connect:", "Bad connection return code =", rc)

    def on_disconnect(self, client, userdata, flags, rc = 0):
        print(self.printPrefix + ":on_disconnect:", "Disconnected result code", str(rc))

    def on_log(self, client, userdata, level, buf):
        print(self.printPrefix + ":on_log:", buf)

    def on_publish(self, client,userdata,result):
        print(self.printPrefix + ":on_publish:", result)

    ###############################################################

    ## callable funcions ##

    def start(self):
        print(self.printPrefix, "start connection and loop...")
        self.client.connect(self.host, keepalive=self.keepAlive)
        self.client.loop_start()
        time.sleep(2)
        print(self.printPrefix, "start successful")
    
    def stop(self):
        print(self.printPrefix, "terminating connection and loop...")
        self.client.loop_stop()
        self.client.disconnect()
        print(self.printPrefix, "client disconnected, terminated")

    def publish(self, topic, data, retain=True):
        print(self.printPrefix, "publishing ", topic, " = ", data, " ...")
        self.client.publish(topic, data, self.qos, retain)
    
    def publishWithCallback(self, topic, _callback = None):
        data = _callback()
        self.publish(topic, data)
