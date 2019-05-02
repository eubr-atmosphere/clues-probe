import json
import requests
import time
from tmalibrary.probes import *
from conf import *

def check_clues_status():
   #clues_url = 'http://localhost:8000/reports/cluesdata.json?secret=not_very_secret_token'
   clues_data = requests.get(CLUES_ENDPOINT).text

   # parse clues_data:
   clues_info = json.loads(clues_data)

   hosts = clues_info["hostevents"]
   free_cpus = 0
   used_cpus = 0

   # CLUES states:
   # ERROR = -2
   # UNKNOWN = -1
   # IDLE = 0
   # USED = 1
   # OFF = 2
   # POW_ON = 3
   # POW_OFF = 4
   # ON_ERR = 5
   # OFF_ERR = 6
   # Consider only status 0,1,3 and 4 to count used and free cpus

   for node, events in hosts.items():
     if events[-1]["state"] in range (0,4) and events[-1]["state"] != 2:
        used_cpus += events[-1]["slots_used"]
        free_cpus += events[-1]["slots"]-events[-1]["slots_used"]

   return used_cpus, free_cpus

def check_deployment_change():
   #clues_url = 'http://localhost:8000/reports/cluesdata.json?secret=not_very_secret_token'
   clues_data = requests.get(CLUES_ENDPOINT).text

   # parse clues_data:
   clues_info = json.loads(clues_data)
   #how to know if a change has ben produced? I need to store the last status for that
   return False

def create_message():
   timestamp = int(time.time())
   # ask CLUES the status of the cluster
   (used_cpus, free_cpus) = check_clues_status()

   # TODO: need to change the probeId, resourceId and messageId
   # probeId: obtained during authentication HOW?
   # resourceId: identifies the resource that is the subject of the attached data
   # messageId: control info
   message = Message(probeId=1, resourceId=101098, messageId=0, sentTime=timestamp, data=None)

   # append measurement of used cpus data to message
   dt = Data(type="measurement", descriptionId=1, observations=None)
   obs = Observation(time=timestamp, value=used_cpus)
   dt.add_observation(observation=obs)

   # append data to message
   message.add_data(data=dt)

   # append measurement of free cpus data to message
   dt = Data(type="measurement", descriptionId=2, observations=None)
   obs = Observation(time=timestamp, value=free_cpus)
   dt.add_observation(observation=obs)

   # append data to message
   message.add_data(data=dt)

   # TODO: Check if the infrastructure has been modified and inform of that change
   has_infrastructure_changed = check_deployment_change()
   if has_infrastructure_changed:
      # append deployment change event data to message
      dt = Data(type="event", descriptionId=3, observations=None)
      obs = Observation(time=timestamp, value=-1)
      dt.add_observation(observation=obs)

      # append data to message
      message.add_data(data=dt)

   # return message formatted in json
   return json.dumps(message.reprJSON(), cls=ComplexEncoder)


if __name__ == '__main__':
    #TODO: read the monitor URL from the conf file
    #url = 'http://158.42.104.30:32025/monitor'
    #url = str(sys.argv[1] + '')
    url = MONITOR_ENDPOINT
    communication = Communication(url)
    while 1:
       message_formated = create_message()
       response = communication.send_message(message_formated)
       time.sleep(1)
       print (response.text)

