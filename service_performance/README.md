# Service Performance: CLUES Probe for TMA-Monitor

CLUES probe for `TMA Monitor` developed in `Python`. CLUES is the elasticity manager of the clusters launched by EC3 inside the ATMOSPHERE project. This probe calculates average time to power on a new node in the cluster. This time includes the time to deploy the new VM and the time to configure the VM to behave as a working node of the cluster. Then, it calculates the standard deviation and returns the coefficient of variation to detect possible anomalies when powering on a node.


## Prerequisites
The probe uses some python libraries that must be installed:

``` 
pip3 install requests
pip3 install tmalibrary
pip3 install wget
pip3 install pycrypto
```

The probe is deployed as a `docker` container so, `docker` is mandatory. 

## Usage

Before starting probe, you will need to configure the properties value in the configuration file. The monitor endpoint should be specified, as the CLUES endpoint.

Also, before building the `docker` image of the probe, you will need to obtain the digital certificate of the Monitor by executing the following command:

```
openssl s_client -showcerts -connect <monitor_IP>:<monitor_port> </dev/null 2>/dev/null|openssl x509 -outform PEM >cert.pem
```

Substitute the certificate you download from this repo by the obtained certificate from the monitor.

Then, you should build the `docker` image that will be used by the probe. You should do that by running the following commands on the Kubernetes Worker node:

```
cd service_performance/
sh build.sh
```

Finally, to deploy the probe, you should run the yaml file on the Kubernetes Master machine:

```
kubectl create -f service-performance.yaml
```
