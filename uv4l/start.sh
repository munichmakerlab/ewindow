#!/bin/sh -ex


curl "http://localhost:1337/janus?gateway_url=http%3A%2F%2F10.80.41.36%3A8088&gateway_root=%2Fjanus&room=1234&room_pin=adminpwd&username=foo&publish=1&vformat=60&hw_vcodec=0&subscribe=1&reconnect=1&action=Start"

curl "https://existence.strfry.org:1337/janus?gateway_url=http%3A%2F%2F10.80.41.36%3A8088&gateway_root=%2Fjanus&room=1234&room_pin=adminpwd&username=bar&token=&proxy_host=&proxy_port=80&proxy_password=&proxy_bypass=&publish=1&vformat=60&hw_vcodec=0&subscribe=1&reconnect=1&action=Start"
