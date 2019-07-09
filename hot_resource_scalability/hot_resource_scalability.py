import json
import requests
import time
from tmalibrary.probes import *
from conf import *

def check_clues_cpus_status():
   #clues_url = 'http://localhost:8000/reports/cluesdata.json?secret=not_very_secret_token'
   clues_data = requests.get(CLUES_ENDPOINT).text

   # parse clues_data:
   clues_info = json.loads(clues_data)

   hosts = clues_info["hostevents"]
   free_cpus = 0
   used_cpus = 0

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
   # Consider only status 0,1,3 to count used and free cpus

   for node, events in hosts.items():
     if events[-1]["state"] in range (0,3) and events[-1]["state"] != 2:
        used_cpus += events[-1]["slots_used"]
        free_cpus += events[-1]["slots"]-events[-1]["slots_used"]

   return used_cpus, free_cpus


def check_clues_mem_status():
   #clues_url = 'http://localhost:8000/reports/cluesdata.json?secret=not_very_secret_token'
   clues_data = requests.get(CLUES_ENDPOINT).text

   # parse clues_data:
   clues_info = json.loads(clues_data)

   hosts = clues_info["hostevents"]
   free_mem = 0
   used_mem = 0

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
   # Consider only status 0,1,3 to count used and free cpus

   for node, events in hosts.items():
     if events[-1]["state"] in range (0,3) and events[-1]["state"] != 2:
        used_mem += events[-1]["memory_used"]
        free_mem += events[-1]["memory"]-events[-1]["memory_used"]

   return used_mem, free_mem


def create_message(messageId):
   timestamp = int(time.time())
   # ask CLUES the status of the cluster
   (used_cpus, free_cpus) = check_clues_cpus_status()
   (used_mem, free_mem) = check_clues_mem_status()

   # Calculate % of used and free CPU
   total_cpu = used_cpus + free_cpus
   used_cpu_pct = (used_cpus * 100) / float(total_cpu)
   free_cpu_pct = (free_cpus * 100) / float(total_cpu)

   # Calculate % of used and free Memory
   total_mem = used_mem + free_mem
   used_mem_pct = (used_mem * 100) / float(total_mem)
   free_mem_pct = (free_mem * 100) / float(total_mem)


   # TODO: need to change the probeId, resourceId and messageId
   # probeId: obtained during authentication HOW?
   # resourceId: identifies the resource that is the subject of the attached data
   # messageId: secuencia de numeros generada por el probe, de forma creciente

   # Create CPU message
   messagecpu = Message(probeId=1, resourceId=101098, messageId=messageId, sentTime=timestamp, data=None)

   # append measurement of used cpus data to message
   dt = Data(type="measurement", descriptionId=1, observations=None)
   obs = Observation(time=timestamp, value=used_cpus_pct)
   dt.add_observation(observation=obs)

   # append data to message
   messagecpu.add_data(data=dt)

   # append measurement of free cpus data to message
   dt = Data(type="measurement", descriptionId=2, observations=None)
   obs = Observation(time=timestamp, value=free_cpus_pct)
   dt.add_observation(observation=obs)

   # append data to message
   messagecpu.add_data(data=dt)

   # Create memory message
   messagemem = Message(probeId=1, resourceId=101099, messageId=messageId+1, sentTime=timestamp, data=None)

   # append measurement of used memory data to message
   dt = Data(type="measurement", descriptionId=3, observations=None)
   obs = Observation(time=timestamp, value=used_mem_pct)
   dt.add_observation(observation=obs)

   # append data to message
   messagemem.add_data(data=dt)

   # append measurement of free memory data to message
   dt = Data(type="measurement", descriptionId=3, observations=None)
   obs = Observation(time=timestamp, value=free_mem_pct)
   dt.add_observation(observation=obs)

   # append data to message
   messagemem.add_data(data=dt)

   return json.dumps(messagecpu.reprJSON(), cls=ComplexEncoder), json.dumps(messagemem.reprJSON(), cls=ComplexEncoder)


if __name__ == '__main__':
    #url = str(sys.argv[1] + '')
    url = MONITOR_ENDPOINT
    communication = Communication(url)
    messageId = 0
    while 1:
       (message_cpu, message_mem) = create_message(messageId)
       messageId +=2
       responsecpu = communication.send_message(message_cpu)
       responsemem = communication.send_message(message_mem)
       time.sleep(10)
       print (responsecpu.text)
       print (responsemem.text)
