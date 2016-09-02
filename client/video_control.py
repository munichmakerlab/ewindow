import os
import time

uv4l_address = 'http://localhost:1337/janus'
local_janus_address = 'localhost:8088'


def connect_local():
  os.system('svc -du /etc/service/janus')
  connect_remote(local_janus_address)

def connect_remote(janus_address):
  os.system('svc -du /etc/service/uv4l')

  time.sleep(1)
  _launch_uv4l(janus_address)


def disconnect(caller_data):
  os.system('svc -dk /etc/service/janus')
  os.system('svc -dk /etc/service/uv4l')


import requests

def _launch_uv4l(url):
  args = {
    'action' : 'Start',
    'gateway_url' : url,
    'gateway_root' : '/janus',
    'room' : '1234',
    'room_pin' : 'adminpwd',
    
    'publish' : '1',
    'subscribe' : '1',
    'reconnect' : '1',
    
    'vformat' : '60',
    'hw_vcodec' : '0', #TODO: Try it with 1
    
#    'username' : 'bar',
#    'token' : '',
  }
  response = requests.get(local_address, params=args)

  print response, dir(response)
  
  if response.status_code != 200 or 'Error' in response.text:
    raise Exception('Unexpected UV4L Error')
