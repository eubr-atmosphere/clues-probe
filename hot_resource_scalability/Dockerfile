FROM python:2.7-alpine3.8


WORKDIR	/hot-resource-scalability

COPY 	cert.pem 	/hot-resource-scalability
COPY 	conf.py 		/hot-resource-scalability
COPY 	hot_resource_scalability.py 		/hot-resource-scalability

RUN pip install requests
RUN pip install tmalibrary
RUN pip install wget


