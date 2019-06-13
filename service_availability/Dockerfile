FROM python:2.7-alpine3.8


WORKDIR	/service-availability

COPY 	cert.pem 	/service-availability
COPY 	conf.py 		/service-availability
COPY 	service-availability.py 		/service-availability

RUN pip install requests
RUN pip install tmalibrary
RUN pip install wget


