# CLUES Probe for TMA-Monitor

CLUES probe for `TMA Monitor` developed in `Python`. CLUES is the elasticity manager of the clusters launched by EC3 inside the ATMOSPHERE project. This probe obtains the values of used and free CPUs in the cluster by processing the CLUES DB.


## Prerequisites

The probe is deployed as a `docker` container so, `docker` is mandatory. 

## Usage

Before starting probe, you will need to configure the properties value in the configuration file. The monitor endpoint should be specified.

Also, you should build the `docker` image that will be used by the probe. You should do that by running the following commands on the Kubernetes Worker node:

```cd clues-probe/
sh build.sh
```

To deploy the probe, you should run the yaml file on the Kubernetes Master machine:

```kubectl create -f clues-probe.yaml
```
