import paho.mqtt.client as paho
import config

# from transitions import Machine

import os, sys, inspect
from transitions import *
from transitions.extensions import GraphMachine
from IPython.display import Image, display, display_png
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

states=['new', 'offline', 'online', 'calling', 'ringing', 'caller', 'callee']

transitions = [
    { 'trigger': 'initialize', 'source': 'new',     'dest': 'offline',    'prepare': 'init' },
    { 'trigger': 'connect',    'source': 'offline', 'dest': 'online',  'conditions': 'toconnect' },

    { 'trigger': 'disconnect', 'source': 'online',  'dest': 'offline', 'before': 'todisconnect' },
    { 'trigger': 'ring',       'source': 'online',  'dest': 'ringing', 'after':  'toring' },

    { 'trigger': 'caller',   'source': 'calling', 'dest': 'caller' },
    { 'trigger': 'rejected', 'source': 'caller',  'dest': 'online', 'after':  'torejected' },
    { 'trigger': 'hangup',   'source': 'caller',  'dest': 'online' },
    { 'trigger': 'hangup',   'source': 'callee',  'dest': 'online' },

    { 'trigger': 'call',     'source': 'online',  'dest': 'calling',  'conditions': 'tocall'  },

    { 'trigger': 'pickup',   'source': 'ringing', 'dest': 'callee' },
    { 'trigger': 'reject',   'source': 'ringing', 'dest': 'online' },
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
    caller = None
    callee = None

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
        logging.info("Outgoing call to %s", target)
        self.callee = target

    def toring(self, target):
        logging.info("Incoming call from %s", target)
        self.caller = target
        # TODO : callback to visualize ring

    def torejected(self):
        logging.info("Rejecting call from %s", self.callee)
        self.callee = None

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
            caller_data = json.loads(msg.payload)

            if action_node == "call":
                if self.stats == "call":
                    # TODO : knocking
                    rejectCall(self.mqttc, caller_data.id)

                elif self.stats == "ringing":
                    # TODO : knocking
                    rejectCall(self.mqttc, caller_data.id)

                elif self.stats == "calling":
                    # TODO : knocking
                    rejectCall(self.mqttc, caller_data.id)

                elif self.stats == "caller":
                    # TODO : knocking
                    rejectCall(self.mqttc, caller_data.id)

                elif self.stats == "callee":
                    # TODO : knocking
                    rejectCall(self.mqttc, caller_data.id)

                elif self.stats == "online":
                    self.ring(caller_data.id)
                    pass

            elif action_node == "answer":
                if self.state != "caller":
                    logger.warning("%s is answering without call request", caller_data.id)
                    return

                if  self.callee != caller_data.id:
                    logger.warning("%s is answering without but %s was called", caller_data.id, self.callee)
                    return

                if caller_data.action == "reject":
                    self.rejected()

                elif caller_data.action == "accept":
                    self.caller()

                elif caller_data.action == "hangup":
                    self.hangup()


    def on_mqttlog(self, client, userdata, level, buf):
        logging.debug(buf)

    def on_mqttsubscribe(self, mosq, obj, mid, granted_qos):
        logging.info("Subscribed: %s %s", str(mid), str(granted_qos))

    def on_mqttdisconnect(self, client, userdata, rc):
        logging.warning("Disconnected (RC %s)", str(rc))


client = EWindow()

# Initialize
machine = Machine(client, states=states, transitions=transitions, initial='new')
machine.graph.draw('my_state_diagram.png', prog='dot')

