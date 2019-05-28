import json
import requests
import time
import sys, subprocess
from tmalibrary.probes import *
from conf import *

def runcommand(command):
    try:
        p=subprocess.Popen(command, stdout=subprocess.PIPE, shell=True, stderr=subprocess.PIPE)
        (out, err) = p.communicate()
        if p.returncode != 0:
            raise Exception("return code: %d\nError output: %s" % (p.returncode, err))
        return out
    except Exception as e:
        raise Exception("Error executing '%s': %s" % (" ".join(command), str(e)))


def calculate_values_cpu_mem():
   # ask CLUES the current status of the cluster
   output = runcommand("clues status")

   # process the output
   i=0
   lines = len(output.split('\n'))
   cpu_used = 0
   mem_used = 0
   cpu_total = 0
   mem_total = 0

   for line in output.splitlines():
      i +=1
      # we remove the headers of the output and the last blank line
      if i>=3 and i < lines-1:
          node = line.split()
          node_used_resources = node[4].split(",")
          node_total_resources = node[5].split(",")
          cpu_used += float(node_used_resources[0])
          mem_used += float(node_used_resources[1])
          cpu_total += float(node_total_resources[0])
          mem_total += float(node_total_resources[1])

   return cpu_used, mem_used, cpu_total, mem_total


def create_message(messageId):
   timestamp = int(time.time())
   # ask CLUES the status of the cluster
   (used_cpus, used_mem, total_cpus, total_mem) = calculate_values_cpu_mem()

   # Calculate % of used CPU and mem
   used_cpu_pct = (used_cpus * 100) / float(total_cpus)
   used_mem_pct = (used_mem * 100) / float(total_mem)

   # TODO: need to change the probeId, resourceId and messageId
   # probeId: obtained during authentication HOW?
   # resourceId: identifies the resource that is the subject of the attached data
   # messageId: secuencia de numeros generada por el probe, de forma creciente
   message = Message(probeId=1, resourceId=101098, messageId=messageId, sentTime=timestamp, data=None)

   # append measurement of used cpus data to message
   dt = Data(type="measurement", descriptionId=1, observations=None)
   obs = Observation(time=timestamp, value=used_cpu_pct)
   dt.add_observation(observation=obs)
   message.add_data(data=dt)

   # append measurement of used memory data to message
   dt = Data(type="measurement", descriptionId=2, observations=None)
   obs = Observation(time=timestamp, value=used_mem_pct)
   dt.add_observation(observation=obs)
   message.add_data(data=dt)

   # Add to the message the static values of total CPU and total Mem
   # append measurement of total memory data to message
   dt = Data(type="measurement", descriptionId=3, observations=None)
   obs = Observation(time=timestamp, value=total_mem)
   dt.add_observation(observation=obs)
   message.add_data(data=dt)

   # append measurement of total cpus data to message
   dt = Data(type="measurement", descriptionId=4, observations=None)
   obs = Observation(time=timestamp, value=total_cpus)
   dt.add_observation(observation=obs)
   message.add_data(data=dt)

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
       time.sleep(10)
       print (response.text)
