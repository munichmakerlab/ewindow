import paho.mqtt.client as paho
import config

from transitions import Machine
from threading import Timer
from time import sleep

import logging
import socket
import uuid
import json
import video_control

logging.basicConfig(format='[%(levelname)s] %(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)

items = {}
topics = []


 # The states

#(self, source, dest, conditions=None, unless=None, before=None, after=None, prepare=None)

states=['new', 'offline', 'online', 'calling', 'ringing', 'call']

transitions = [
    { 'trigger': 'initialize', 'source': 'new',     'dest': 'offline',    'prepare': 'init' },
    { 'trigger': 'connect',    'source': 'offline', 'dest': 'online',  'conditions': 'toconnect' },

    { 'trigger': 'disconnect', 'source': 'online',  'dest': 'offline', 'before': 'todisconnect' },
    { 'trigger': 'call',       'source': 'online',  'dest': 'calling',  'conditions': 'tocall'  },
    # { 'trigger': 'ring',       'source': 'online',  'dest': 'ringing' },

    # { 'trigger': 'incall',        'source': 'calling', 'dest': 'call' },
    # { 'trigger': 'rejected',      'source': 'calling', 'dest': 'online' },

    # { 'trigger': 'incall',        'source': 'ringing', 'dest': 'call' },
    # { 'trigger': 'reject',        'source': 'ringing', 'dest': 'online' },

    # { 'trigger': 'hangup',        'source': 'call',    'dest': 'online' }
]

def setupCall(client, id):
    data = { "id": self.uuid }
    client.publish("%s/%s/call" % (config.topic_root, id), json.dumps(data) )

def rejectCall(client, id):
    data = { "id": self.uuid, "action": "reject" }
    client.publish("%s/%s/answer" % (config.topic_root, id), json.dumps(data) )

def acceptCall(client, id, janusip):
    data = { "id": self.uuid, "action": "accept", "janus": janusip }
    client.publish("%s/%s/answer" % (config.topic_root, id), json.dumps(data) )

def hangupCall(client, id):
    data = { "id": self.uuid, "action": "hangup" }
    client.publish("%s/%s/answer" % (config.topic_root, id), json.dumps(data) )

class EWindow(object):

    nodes_dict = {}

    def init(self):
        self.uuid = str(uuid.uuid4())
        self.node_path = config.topic_root + "/" + self.uuid

        logging.info("Initializing MQTT (%s)", self.uuid)
        self.mqttc = paho.Client(self.uuid)
        self.mqttc.username_pw_set(config.broker["user"], config.broker["password"])

        self.mqttc.on_connect = self.on_mqttconnect
        self.mqttc.on_message = self.on_mqttmessage
        self.mqttc.on_disconnect = self.on_mqttdisconnect
        self.mqttc.on_subscribe = self.on_mqttsubscribe
        self.mqttc.on_log = self.on_mqttlog

        # Set will to delete node id from addressbook
        self.mqttc.will_set(self.node_path, None, 0, True)
        True

    def toconnect(self):
        logging.info("Connecting to Broker %s:%d", config.broker["hostname"], config.broker["port"])
        try:
            self.mqttc.connect(config.broker["hostname"], config.broker["port"], keepalive=config.keepalive)
            self.mqttc.loop_start()

        except:
            logging.warning("Connection failed.")
            return False

        return True

    def todisconnect(self):
        logging.info("Disconnecting")
        try:
            self.mqttc.publish(self.node_path, None, 1, True)
            self.mqttc.loop_stop()
            self.mqttc.disconnect()

        except:
            logging.warning("Disconnect failed.")
            return False

        return True

    def tocall(self, target):
        logging.info("Calling %s", target)

    def on_mqttconnect(self, mosq, obj, rc, test):
        logging.info("Connect with RC %s", str(rc))

        status = {
            "ip": socket.gethostbyname(socket.gethostname()),
            "status": "ready",
            "name": config.node_name
        }
        self.mqttc.publish(self.node_path, json.dumps(status), 1, True)
        self.mqttc.subscribe(config.topic_root + "/+", 1)
        self.mqttc.subscribe("%s/%s" % (self.node_path, config.node_call), 1)
        self.mqttc.subscribe("%s/%s" % (self.node_path, config.node_answer), 1)

    def on_mqttmessage(self, mosq, obj, msg):
        logging.info("Message %s [%s]: %s", msg.topic, str(msg.qos), str(msg.payload))

        if not msg.topic.startswith(config.topic_root):
            return

        node = msg.topic[len(config.topic_root)+1:].split("/")
        node_uuid   = node[0]

        # managing the phonebook
        if node_uuid != self.uuid:
            if len(msg.payload) > 0:
                # add node to local adressbook
                self.nodes_dict[node_uuid] = json.loads(msg.payload)
            else:
                # remove old node from dict
                try:
                    self.nodes_dict.pop(node_uuid)
                except NameError:
                    pass
            return

        # call interaction
        if len(node) == 2:
            action_node = node[1]

            if action_node == "call":
                caller_data = json.loads(msg.payload)

                if self.stats == "call"
                    rejectCall(self.mqttc, caller_data.id)

                elif self.stats == "ringing"
                    rejectCall(self.mqttc, caller_data.id)

                elif self.stats == "calling"
                    rejectCall(self.mqttc, caller_data.id)

                elif self.stats == "online"
                    # TODO: klingeln
                    pass

            elif action_node == "answer":
                # check if I setup a call to the answering id
                # ignore if not

                # if reject then cancel call

                # if accept and not in call then startup janus

                # if hangup and in call then close janus


    def on_mqttlog(self, client, userdata, level, buf):
        logging.debug(buf)

    def on_mqttsubscribe(self, mosq, obj, mid, granted_qos):
        logging.info("Subscribed: %s %s", str(mid), str(granted_qos))

    def on_mqttdisconnect(self, client, userdata, rc):
        logging.warning("Disconnected (RC %s)", str(rc))


client = EWindow()

# Initialize
machine = Machine(client, states=states, transitions=transitions, initial='new')

