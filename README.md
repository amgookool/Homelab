# Self Hosted VPN

The two self-hosted VPN server application that can be selected are:

- [Wireguard](https://www.wireguard.com/)
- [OpenVPN](https://openvpn.net/)

I would suggest setting up a wireguard server as it is much faster than OpenVPN and it does't add as much data overhead as OpenVPN.

This was an article that guided my decision.(<https://www.top10vpn.com/guides/wireguard-vs-openvpn/>)

## Setup

Both WireGuard and OpenVPN server requires a linux operating system. Since NUC machine was considered to run the VPN server, it is suitable to use a containerized instance of the wireguard application. This docker compose file should be run in a ```WSL``` linux distro instance. This is because wireguard requires kernel modules and network-related admin tasks.

```docker-compose
version: '3.8'
services:
  wireguard:
    image: linuxserver/wireguard:latest
    container_name: wireguard
    restart: unless-stopped
    ports:
      - 51820:51820/udp
    sysctls:
      - net.ipv4.conf.all.src_valid_mark=1
    volumes:
      - /opt/wireguard-server/config:/config
      - /lib/modules:/lib/modules
    cap_add:
      - NET_ADMIN
      - SYS_MODULE
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=America/La_Paz
      - LOG_CONFS=true
      - ALLOWEDIPS=0.0.0.0/0
      - SERVERURL=auto
      - SERVERPORT=51820 
      - PEERS=5 #number of client (peer1, peer2, etc)
      - PEERDNS=auto 
      - INTERNAL_SUBNET=192.168.80.0 #should be an offshoot of private ip address
```

Note: You can get the ```uid``` and ```gid``` of the user using the command:

```bash
id <username>
```

## Router Configurations

On your router, you will need to forward the port ```51820``` to the NUC machine. This is done by accessing the router's admin page and navigating to the port forwarding section. The NUC machine should have a static IP address. This can be done by setting the IP address of the NUC machine to a static IP address in the router's admin page. Ensure that UDP is selected as the protocol.

### Digicel Router Configuration

On the Digicel router, the port forwarding section is located under the ```Forward Rules``` tab. The ```PCP Configuration``` section should be selected and you will see all the forwarding rules.Click on ```New``` to create a new rule.

The following settings should be used for UDP port forwarding rule:

- Internal IPv4 Address: The static IP address of the NUC machine
- Internal Port: 51820
- Protocol: UDP
- Required External IPv4 Address: Public IP address of the router
- External Port: 51820
- Allow PCP Port Proposals: Yes

The following settings should be used for TCP port forwarding rule:

- Internal IPv4 Address: The static IP address of the NUC machine
- Internal Port: 51820
- Protocol: TCP
- Required External IPv4 Address: Public IP address of the router
- External Port: _port of the dynamically assigned UDP rule_
- Allow PCP Port Proposals: No

**Note for UDP:** The ```Allow PCP Port Proposals``` would set its own public port (Not what we specified) and setting Allow PCP Port Proposals to No would cause the forwarding to fail. Take not of this port number. We will need it for the client configuration.

Note: If the Wireguard server shuts down, the port number will change and you will need to modify the TCP rule to match the new port number. Additionally, the client configuration file will need to be updated with the new port number.

## Client Configuration

The docker container will generate the client configurations within the ```/config``` directory. The client configs will have a naming scheme like peer1.conf, peer2.conf, etc. The client configuration file should be downloaded and imported into the wireguard client application.

We can copy the client configurations to the local machine from the docker container  using the following command:

```bash
docker cp wireguard:/config/peer<integer> .
```

The above command will copy the client config folder to your current working directory.

If you are using a Digicel router, you will need to change the port number in the client config endpoint to match the port number of the dynamically assigned UDP rule.

Next, using the [wireguard client application](https://www.wireguard.com/install/), import the client configuration file and connect to the VPN server.
