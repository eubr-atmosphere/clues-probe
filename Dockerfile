FROM python:2.7-alpine3.8


WORKDIR	/clues-probe

COPY 	cert.pem 	/clues-probe
COPY 	clues-probe.py 		/clues-probe

RUN pip install requests
RUN pip install tmalibrary
RUN pip install wget


