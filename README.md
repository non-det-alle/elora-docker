# ELoRa: LoRaWAN emulator for ChirpStack network server #

This is a traffic emulator for the [Chirpstack server stack](https://www.chirpstack.io/ "ChirpStack, open-source LoRaWAN® Network Server"). 

The [code inside the docker image](https://github.com/non-det-alle/lorawan.git) is a direct extension of the ns-3 [LoRaWAN module](https://github.com/signetlabdei/lorawan "LoRaWAN ns-3 module").

This module can be used to simulate in real-time multiple devices and gateways sharing a radio channel with very high flexibility in terms of possible configurations. LoRaWAN traffic is then UDP-encapsulated by gateways and forwarded outside the simulation. If a Chirpstack network server is in place, it will think the traffic is coming from a real network. All Class A MAC primitives used in the UE868 region are supported: radio transmission parameters of simulated devices can be changed by the downlink LoRaWAN traffic of the real server. 

In addition to what is provided by the original LoRaWAN module, the following changes/additions were made:

* A gateway application implementing the [UDP forwarder protocol](https://github.com/Lora-net/packet_forwarder/blob/master/PROTOCOL.TXT "Semtech packet forwarder implementation") running on real gateways
* An helper to register devices and gateways in the server using the included [REST API](https://github.com/chirpstack/chirpstack-rest-api "ChirpStack gRPC to REST API proxy")
* Cryptographyc libraries to compute the Meassage Integrity Code (MIC) and encryption of packets for devices to be recognised by the server
* Many improvements and corrections of features of the original module, such that traffic could be transparently be accepted by the server
* The [`elora-example`](/elora-example/) to show a complete scenario using the traffic generator

## Prerequisites ##

To use the simulator with docker you need to do/know the following:

* Docker and docker compose need to be installed on your system
* The ChirpStack server's components needs to be running somewhere reachable by the simulation via the host network. In particular, a ChirpStack Gateway Bridge needs to be listening to port 1700 (default config) on the same host you use to run the simulator image
* The simulator works as is with the default configuration of ChirpStark v4. It has been tested with the local [docker-compose installation](https://www.chirpstack.io/docs/getting-started/docker.html "Chirpstack docs: Quickstart Docker Compose") of the server. To run a distributed version of the setup, the IP address of the server's REST API needs to be changed accordingly in [`configuration.toml`](/configuration.toml), and a ChirpStark Gateway Bridge needs to remain co-located on the same machine of the ELoRa container
* An authentification token needs to be generated in the server UI (API keys section), and needs to be copy-pasted in [`configuration.toml`](/configuration.toml)

## Usage ##

The image can be run with `docker compose up`.

More details on configurations and on the provided example's parameters can be found in [`configuration.toml`](/configuration.toml). You can develop your own simulation scenario by editing the default example file in the folder [`elora-example`](/elora-example/).

We support the developement phylosophy of ns-3. Feel free to contribute by forking [the module repository](https://github.com/non-det-alle/lorawan.git). You can add your own repo as a git submodule in the [`build` directory](/build/), edit the [`Dockerfile`](/build/Dockerfile) accordingly, and run `docker compose build` in the project root directory.

For more information on how to use the underlying LoRaWAN module refer to the [original module readme](https://github.com/signetlabdei/lorawan/blob/e8f7a21044418e92759d5c7c4bcab147cdaf05b3/README.md "LoRaWAN ns-3 module README").

## Getting help ##

If you need any help, feel free to open an issue here or on the [module repository](https://github.com/non-det-alle/lorawan.git).
