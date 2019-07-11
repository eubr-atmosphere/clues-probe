import json
import requests
import time
import sys, subprocess
from tmalibrary.probes import *
from conf import *

def pingclues(command):
    try:
        p=subprocess.Popen(command, stdout=subprocess.PIPE, shell=True, stderr=subprocess.PIPE)
        (out, err) = p.communicate()
        # Could not connect to CLUES server http://localhost:8000/RPC2 (please, check if it is running)
        if p.returncode != 0 or "not connect" in out :
#            raise Exception("return code: %d\nError output: %s" % (p.returncode, err))
            return False
        return True
    except Exception as e:
#        raise Exception("Error executing '%s': %s" % (" ".join(command), str(e)))
        return False

def create_message(messageId, cluesavailability):
   timestamp = int(time.time())

   # TODO: need to change the probeId, resourceId and messageId
   # probeId: obtained during authentication HOW?
   # resourceId: identifies the resource that is the subject of the attached data
   # messageId: secuencia de numeros generada por el probe, de forma creciente
   # estos datos los tengo que solicitar a UC cuando registremos el probe
   message = Message(probeId=1, resourceId=101098, messageId=messageId, sentTime=timestamp, data=None)

   # append measurement of % failure of CLUES to message
   dt = Data(type="measurement", descriptionId=1, observations=None)
   obs = Observation(time=timestamp, value=cluesavailability)
   dt.add_observation(observation=obs)

   # append data to message
   message.add_data(data=dt)

   # return message formatted in json
   return json.dumps(message.reprJSON(), cls=ComplexEncoder)


if __name__ == '__main__':
    #url = str(sys.argv[1] + '')
    url = MONITOR_ENDPOINT
    communication = Communication(url)
    messageId = 0
    totalCalls = 1
    failures = 0
    while 1:
       availability = pingclues("clues status")
       if availability == False :
           failures +=1
       cluesavailability = (failures * 100) / float(totalCalls) 
       message_formated = create_message(messageId, cluesavailability)
       response = communication.send_message(message_formated)
       messageId +=1
       totalCalls +=1
       time.sleep(60)
       print (response.text)

