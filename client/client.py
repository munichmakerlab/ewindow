#!/usr/bin/env python

import paho.mqtt.client as paho

import config

from threading import Timer
from time import sleep
import logging
import socket
import uuid
import json
import video_control


def on_connect(mosq, obj, rc):
    logging.info("Connect with RC " + str(rc))

    status = {
        "ip": socket.gethostbyname(socket.gethostname()),
        "status": "ready",
        "name": config.node_name
    }
    mqttc.publish(node_path, json.dumps(status), 1, True)
    mqttc.subscribe(config.topic_root + "/+", 1)
    mqttc.subscribe("%s/%s" % (node_path, config.node_call), 1)
    mqttc.subscribe("%s/%s" % (node_path, config.node_answer), 1)


def on_message(mosq, obj, msg):
    global state_in_call

    logging.info(msg.topic + " [" + str(msg.qos) + "]: " + str(msg.payload))
    # remove prefix from topic.
    if msg.topic.startswith(config.topic_root):
        node = msg.topic[len(config.topic_root)+1:]
        node_uuid = node.split("/")[0]
        if node_uuid == uuid:
            # Stuff happens on the local node
            action_node = msg.topic[len(node_path)+1:]
            if action_node == "call":
                caller_data = json.loads(msg.payload)
                answer = None

                # implement proper state machine
                ###if state_window_open and not state_in_call:
                    # janus runs on caller, lets connect
                #    answer = json.dumps({"answer": "connecting"})
                #   video_control.connect_to_remote(caller_data)



                mqttc.publish("%s/%s" % (node_path, config.node_answer),answer , 1, True)


            elif action_node == "answer":
                pass



        else:
            # nodes join or leave the network
            if len(msg.payload) > 0:
                # add node to local adressbook
                nodes_dict[node_uuid] = json.loads(msg.payload)
            else:
                # remove old node from dict
                try:
                    nodes_dict.pop(node_uuid)
                except NameError:
                    pass
    else:
        return

    logging.info(str(node))


def on_subscribe(mosq, obj, mid, granted_qos):
    logging.info("Subscribed: "+str(mid)+" "+str(granted_qos))

def on_disconnect(client, userdata, rc):
    mqttc.publish(node_path, None, 1, True)
    logging.warning("Disconnected (RC " + str(rc) + ")")
    if rc <> 0:
        try_reconnect(client)

def on_log(client, userdata, level, buf):
    logging.debug(buf)

def try_reconnect(client, time = 60):
    try:
        logging.info("Trying reconnect")
        client.reconnect()
    except:
        logging.warning("Reconnect failed. Trying again in " + str(time) + " seconds")
        Timer(time, try_reconnect, [client]).start()

logging.basicConfig(format='[%(levelname)s] %(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)

items = {}
topics = []
nodes_dict = {}

uuid = str(uuid.uuid4())
node_path = config.topic_root + "/" + uuid

logging.info("Initializing MQTT (%s)" % uuid)
mqttc = paho.Client(uuid)
mqttc.username_pw_set(config.broker["user"], config.broker["password"])
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_disconnect = on_disconnect
mqttc.on_subscribe = on_subscribe
mqttc.on_log = on_log

# Set will to delete node id from addressbook
mqttc.will_set(node_path, None, 0, True)

# States


try:
    mqttc.connect(config.broker["hostname"], config.broker["port"], keepalive=config.keepalive)

except:
    logging.warning("Connection failed. Trying again in 30 seconds")
    Timer(30, try_reconnect, [mqttc]).start()


logging.info("Entering loop")
mqttc.loop_start()

try:
    # Set open to true, need button handling here
    state_window_open = True

    while True:
        sleep(2)
        print nodes_dict

except KeyboardInterrupt:
    pass

logging.info("Exiting")
mqttc.loop_stop()
