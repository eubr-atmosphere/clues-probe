FROM python:2.7-alpine3.8


WORKDIR	/clues-probe

COPY 	cert.pem 	/clues-probe
COPY 	data.py 		/clues-probe
COPY 	message.py 		/clues-probe
COPY 	observation.py 	/clues-probe
COPY 	communication.py 	/clues-probe

RUN pip install requests
RUN pip install tmalibrary


