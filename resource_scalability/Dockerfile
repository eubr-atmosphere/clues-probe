FROM python:2.7-alpine3.8


WORKDIR	/resource-scalability

COPY 	cert.pem 	/resource-scalability
COPY 	conf.py 		/resource-scalability
COPY 	resource_scalability.py 		/resource-scalability

RUN pip install requests
RUN pip install tmalibrary
RUN pip install wget


