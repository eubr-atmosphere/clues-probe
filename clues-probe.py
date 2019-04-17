from tmalibrary.probes import *
import json
import wget

clues_url = 'http://localhost:8000/reports/cluesdata.json?secret=not_very_secret_token'
clues_data = wget.download(clues_url)
print clues_data