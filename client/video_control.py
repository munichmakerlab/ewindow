def connect_local():
  os.system('svc -u /etc/service/janus')
  os.system('svc -u /etc/service/uv4l')

  time.sleep(1)
  _launch_uv4l('localhost:1337')

def connect_remote(remote_address):
  # Start UV4L
  # Instruct UV4L to connect to remote host

def disconnect(caller_data):
  os.system('svc -d /etc/service/janus')
  os.system('svc -d /etc/service/uv4l')


import requests

def _launch_uv4l(url):
  args - {
    'action' : 'Start',
    'gateway_url' : url,
    'gateway_root' : '/janus',
    'room' : '1234',
    'room_pin' : 'adminpwd',
    
    'publish' : '1',
    'subscribe' : '1',
    'reconnect' : '1'
    
    'vformat' : '60',
    'hw_vcodec' : '0', #TODO: Try it with 1
    
#    'username' : 'bar',
#    'token' : '',
  }
  response = requests.get('http://%s/janus'.format(url), args)
  
  if 'Error' in response.text:
    raise Exception('Unexcepted UV4L Error')
