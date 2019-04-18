import json
import requests
import time
from tmalibrary.probes import *

clues_url = 'http://localhost:8000/reports/cluesdata.json?secret=not_very_secret_token'
clues_data = requests.get(clues_url).text

# parse clues_data:
y = json.loads(clues_data)
print(y["hostevents"])
print(y["hostevents"]["wn1.localdomain"])
print(y["hostevents"]["wn1.localdomain"][4])
print(y["hostevents"]["wn1.localdomain"][4]["slots"])
print(y["hostevents"]["wn1.localdomain"][4]["slots_used"])

def create_message(probeID, resourceID, messageID, setTime, data):
   message = Message(probeID, resourceID, messageID, setTime, data)
   return message

def create_data(type, descriptionId, observations):
   data = Data(type, descriptionId, observations)
   return data

def create_observation(time, value):
   observation = Observation(time, value)
   return observation

mimensaje = create_message(1,1,1,time.time(),None)
print mimensaje.resourceID
