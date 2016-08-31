#!/bin/sh -ex

curl http://10.80.41.36:1337/janus?action=Stop

curl https://existence.strfry.org:1337/janus?action=Stop
