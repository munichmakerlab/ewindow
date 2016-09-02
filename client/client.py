from ewindow import client
from time import sleep

print client.state

client.initialize()

print client.state

client.connect()

print client.state

count = 0

try:

    while True:
        sleep(2)
        count += 1

        if(count < 2):
          print client.nodes_dict

        # if(count == 2):
        #   break

except KeyboardInterrupt:
    pass
