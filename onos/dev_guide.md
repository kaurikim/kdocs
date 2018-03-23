
# Developer Quick Start

```
udo apt-get install software-properties-common -y && \
sudo add-apt-repository ppa:webupd8team/java -y && \
sudo apt-get update && \
echo "oracle-java8-installer shared/accepted-oracle-license-v1-1 select true" | sudo debconf-set-selections && \
sudo apt-get install oracle-java8-installer oracle-java8-set-default -y
```

```
git clone https://gerrit.onosproject.org/onos
cd onos
export ONOS_ROOT=$(pwd)
tools/build/onos-buck build onos --show-output
```

* To run ONOS locally on the development machine, simply run the following command:

```
tools/build/onos-buck run onos-local -- clean debug
```

The above command will create a local installation from the onos.tar.gz 
file (re-building it if necessary) and will start the ONOS server in the 
background. In the foreground, it will display a continuous view of the 
ONOS (Apache Karaf) log file. Options following the double-dash (–) are 
passed through to the ONOS Apache Karaf and can be omitted. Here, the 
clean option forces a clean installation of ONOS and the debug option means 
that the default debug port 5005 will be available for attaching a remote 
debugger.


* To attach to the ONOS CLI console, run:
```
tools/test/bin/onos localhost
```

* To open your default browser on the ONOS GUI page, simply type:
```
tools/test/bin/onos-gui localhost
```

* To start up a Mininet network controlled by an ONOS instance that is already running on your development machine, you can use a command like:
```
sudo mn --controller remote,ip=<ONOS IP address> --topo torus,3,3
```

* To execute ONOS unit tests, including code Checkstyle validation, run the following command:
```
tools/build/onos-buck test
```

* If you want to import the project into IntelliJ, you can generate the hierarchical module structure via the following command:
```
tools/build/onos-buck project
```
Then simply open the onos directory from IntelliJ IDEA.


# Adding ONOS utility scripts and functions to your environment

```
export ONOS_ROOT=~/onos
source $ONOS_ROOT/tools/dev/bash_profile
```

# Development Workflow Options

## Cells and ONOS test scripts

Test Environment Components
An ONOS developer's environment may include the following:

* Development/build machine : for actual code development e.g. running the IDE and building/packaging/deploying ONOS. 
* One or more test deployment VMs : for running ONOS instances
* A Mininet VM : for emulating networks to test with ONOS
* In the above case, the ONOS scripts are run from the development machine, and are directed towards the VMs running on a hypervisor (which can also be on the same machine, or elsewhere). 

Lastly, since a developer may want to test different scenarios against different sets of VMs or servers, ONOS provides the notion of test cells. 


## Using cells

```
$ cell local                                             
ONOS_CELL=local
OCI=192.168.56.101
OC1=192.168.56.101
OC2=192.168.56.102
OCN=192.168.56.103
ONOS_FEATURES=webconsole,onos-api,onos-core,onos-cli,onos-openflow,onos-gui,onos-rest,onos-app-fwd,onos-app-proxyarp,onos-app-tvue
ONOS_NIC=192.168.56.*
```

* OCI : the default target node IP. This is an alias for OC1. 
* OC[1-3] : IP addresses of the VMs hosting ONOS instances. More OC instances may be set, if necessary.
* OCN : IP address of the VM with Mininet
* ONOS_FEATURES : a comma-separated list of bundle names, loaded at startup by an ONOS instance within this cell
* ONOS_NIC : The address block used amongst ONOS instances for inter-controller (clustering) and OpenFlow communication 


## Test VM Setup

ONOS, being an SDN controller authored in Java, can run on a variety of platforms. However, in the interest of focus, the ONOS team engages primarily in testing on Ubuntu server distributions, specifically Ubuntu Server 14.04* LTS 64-bit.

Additionally, the VMs used for running ONOS instances and Mininet can be configured to better mesh with the functionality of the ONOS utility scripts and the test environment:

* Adding two network interfaces : One should be configured to use the host adapter and the other to use either the NAT or Bridged adapter to allow outside access.
* Adding an user named 'sdn' : The scripts check for the environment variable ONOS_USER, and, if it is unset, uses sdn as the default username. 
* Allowing password-less (key-based) login : The scripts rely on ssh and scp for their functions, and this lets one avoid having to type a password each time a script is run.

For password-less login, the onos-push-keys  utility can be used to transfer one's SSH key to the VM.

## Using the Test Environment

Once set up, changes to the codebase can be (relatively) quickly tested in a distributed setting as follows:

1. Make changes to the code
1. Build with mvn clean install
1. Load the cell settings with cell <your_cell_name>
1. Package executables for deployment with onos-package 
1. Deploy to test VMs in the cell
1. For step 5, a developer can take advantage of the OC variables when using onos-install:

```
$ onos-install -f $OC1  #install ONOS to OC1
```

This procedure must be repeated for each target, as onos-install is only capable of handling one target at a time. In ONOS 1.1.0 and later, the onos-group command can be used to automatically target all cell member VMs at once:

```
$ onos-group install -f
```

Utilities such as onos-service also take the --cell argument that enables it to manage all cell members at once. For example, to restart all ONOS instances in a cell:

```
$ onos-service --cell restart
```

# ONOS Software Development

## Template Application Tutorial

### Publish the artifacts to local repository

ONOS project started using BUCK from 1.7.0 hummingbird release. If you want to build ONOS application with maven archetype, you should publish the artifacts to local repository in ~/.m2:

```
onos-buck-publish-local
```

### Generate your ONOS application project

Let's now generate an ONOS project which will be fully compilable and ready to be deployed. Although, you will still have to code up your application, we haven't yet figured out how to generate code that does exactly what you would like it to do (wink). So let's start by running the following in a directory outside of $ONOS_ROOT:

```
mvn archetype:generate -DarchetypeGroupId=org.onosproject -DarchetypeArtifactId=onos-bundle-archetype
```


* https://github.com/kspviswa/myapps.git

