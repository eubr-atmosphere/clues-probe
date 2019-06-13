FROM python:2.7-alpine3.8


WORKDIR	/service-performance

COPY 	cert.pem 	/service-performance
COPY 	conf.py 		/service-performance
COPY 	service-performance.py 		/service-performance

RUN pip install requests
RUN pip install tmalibrary
RUN pip install wget


