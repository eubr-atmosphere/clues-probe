import json
import requests
import time
from tmalibrary.probes import *

def check_used_cpus():
   #TODO: read the clues_url from the conf file
   clues_url = 'http://localhost:8000/reports/cluesdata.json?secret=not_very_secret_token'
   clues_data = requests.get(clues_url).text

   # parse clues_data:
   y = json.loads(clues_data)
   return y["hostevents"]["wn1.localdomain"][4]["slots"]

def check_free_cpus():
   #TODO: read the clues_url from the conf file
   clues_url = 'http://localhost:8000/reports/cluesdata.json?secret=not_very_secret_token'
   clues_data = requests.get(clues_url).text

   # parse clues_data:
   y = json.loads(clues_data)
   return y["hostevents"]["wn1.localdomain"][4]["slots_used"]

def check_deployment_change():
   #TODO: read the clues_url from the conf file
   clues_url = 'http://localhost:8000/reports/cluesdata.json?secret=not_very_secret_token'
   clues_data = requests.get(clues_url).text

   # parse clues_data:
   y = json.loads(clues_data)


def create_message():
   timestamp = int(time.time())
   # TODO: need to change the probeId, resourceId and messageId
   # probeId: obtained during authentication HOW?
   # resourceId: identifies the resource that is the subject of the attached data
   # messageId: control info
   message = Message(probeId=1, resourceId=101098, messageId=0, sentTime=timestamp, data=None)

   # append measurement of used cpus data to message
   dt = Data(type="measurement", descriptionId=1, observations=None)
   obs = Observation(time=timestamp, value=check_used_cpus())
   dt.add_observation(observation=obs)

   # append data to message
   message.add_data(data=dt)

   # append measurement of free cpus data to message
   dt = Data(type="measurement", descriptionId=2, observations=None)
   obs = Observation(time=timestamp, value=check_free_cpus())
   dt.add_observation(observation=obs)

   # append data to message
   message.add_data(data=dt)

   # Check if the infrastructure has been modified and inform of that change
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
    url = str(sys.argv[1] + '')
    communication = Communication(url)
    while 1:
       message_formated = create_message()
       response = communication.send_message(message_formated)
       time.sleep(1)
       print (response.text)

