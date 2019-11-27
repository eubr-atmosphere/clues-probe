# CLUES Probes for TMA-Monitor

CLUES probes for `TMA Monitor` developed in `Python` 3. CLUES is the elasticity manager of the clusters launched by EC3 inside the ATMOSPHERE project. 

The probes for CLUES are:

- hot_resource_scalability: % of used and free CPUs and % of used and free RAM memory without powering on new VMs.
- resource_scalability: % of used CPUs and RAM memory in the cluster, taking into account all the nodes, regardless their state. Also it obtains the total CPU and RAM that the cluster can have.
- service_availability: % Failure of CLUES.
- service_performance: coefficient of variation to detect possible anomalies in the time required for CLUES to provide a new configured node.


## Usage

All probes require the same configuration:

First, they have to run using Python 3. And the python libraries should be installed by using pip3.

Before starting probe, you will need to configure the properties value in the configuration file. The monitor endpoint should be specified, as the CLUES endpoint.

Also, before building the `docker` image of the probe, you will need to obtain the digital certificate of the Monitor by executing the following command:

```
openssl s_client -showcerts -connect <monitor_IP>:<monitor_port> </dev/null 2>/dev/null|openssl x509 -outform PEM >cert.pem
```

Substitute the certificate you download from this repo by the obtained certificate from the monitor.

Then, you should build the `docker` image that will be used by the probe. You should do that by running the following commands on the Kubernetes Worker node:

```
cd <probe_name>/
sh build.sh
```

Finally, to deploy the probe, you should run the yaml file on the Kubernetes Master machine:

```
kubectl create -f <probe_name>.yaml
```
