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

   # CLUES node states:
   # ERROR = -2
   # UNKNOWN = -1
   # IDLE = 0
   # USED = 1
   # OFF = 2
   # POW_ON = 3
   # POW_OFF = 4
   # ON_ERR = 5
   # OFF_ERR = 6

   tdeployment = 0
   tdeployment_total = 0
   count = 0

   for node, events in hosts.items():
      for event in events:
         if event["state"] == 3:
            if events[events.index(event)+1]["state"] == 0:
               tdeployment = events[events.index(event)+1]["t"] - event["t"]
               count += 1
               tdeployment_total += tdeployment

   tmedio = tdeployment_total / float(count)
   print "tiempo medio despliegue WN: " + str(tmedio)
   return tmedio

def create_message(messageId):
   timestamp = int(time.time())
   # ask CLUES the status of the cluster
   deployment_time = check_clues_status()

   # TODO: need to change the probeId, resourceId and messageId
   # probeId: obtained during authentication HOW?
   # resourceId: identifies the resource that is the subject of the attached data
   # messageId: secuencia de numeros generada por el probe, de forma creciente
   message = Message(probeId=1, resourceId=101098, messageId=messageId, sentTime=timestamp, data=None)

   # append measurement of deployment time to message
   dt = Data(type="measurement", descriptionId=1, observations=None)
   obs = Observation(time=timestamp, value=deployment_time)
   dt.add_observation(observation=obs)
   message.add_data(data=dt)

   # return message formatted in json
   return json.dumps(message.reprJSON(), cls=ComplexEncoder)


if __name__ == '__main__':
    #url = str(sys.argv[1] + '')
    url = MONITOR_ENDPOINT
    communication = Communication(url)
    messageId = 0
    while 1:
       messageId +=1
       message_formated = create_message(messageId)
       response = communication.send_message(message_formated)
       time.sleep(60)
       print (response.text)


