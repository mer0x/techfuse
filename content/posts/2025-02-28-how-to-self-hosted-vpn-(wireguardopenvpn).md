---
title: "How to self-hosted VPN (WireGuard/OpenVPN)"
date: 2025-02-28
tags: ["Self-Hosting", "DevOps", "Homelab", "Networking"]
categories: ["IT Tutorials"]
draft: false
---
# How to Self-Host a VPN Using WireGuard/OpenVPN

## Introduction

In today's digital age, privacy and secure access to networks are more important than ever. Whether you're looking to protect your online activities, access geographically restricted content, or securely connect to your home network while away, setting up your own VPN can be an excellent solution. With the rise of services like WireGuard and OpenVPN, self-hosting a VPN is both accessible and highly effective.

This tutorial aims to guide you on how to set up your own VPN server using WireGuard or OpenVPN. By self-hosting, you're not only saving on monthly subscription costs of traditional VPN services, but you're also gaining full control over your data and its privacy.

## Prerequisites

Before we dive into the technical setup, you'll need to have the following:

- A **VPS or a dedicated server** with a public IP address.
- **Basic knowledge of Linux command line**.
- **SSH access** to your server.
- **Docker** installed on your server.
- Optional: A public **domain** (helpful for easier connectivity).
- Optional: **Cloudflare** account for easy DNS management.

## Step-by-Step Implementation

### 1. Choose a VPN Solution

For this tutorial, we'll be looking at two popular open-source options: **WireGuard** and **OpenVPN**. Both have unique benefits:

- **WireGuard**: Known for its performance, simplicity, and modern cryptography. It offers minimal latency and is easy to set up.
- **OpenVPN**: Known for its flexibility and robust security features. It's widely used and battle-tested over the years.

### 2. Install Docker

Ensure your server has Docker installed. If not, you can install Docker using the following command:

```bash
sudo apt update
sudo apt install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker
```

### 3. Set Up the VPN Server

We'll demonstrate how to set up both WireGuard and OpenVPN using Docker.

#### 3.1 Setting Up WireGuard

1. **Create a Docker-Compose File for WireGuard**:

   Create a directory for WireGuard configuration:

   ```bash
   mkdir ~/wireguard
   cd ~/wireguard
   ```

   Create a `docker-compose.yml` file:

   ```yaml
   version: '2.1'
   services:
     wireguard:
       image: linuxserver/wireguard
       container_name: wireguard
       cap_add:
         - NET_ADMIN
         - SYS_MODULE
       environment:
         - PUID=1000
         - PGID=1000
         - TZ=Etc/UTC
         - SERVERURL=your-server-ip
         - SERVERPORT=51820
         - PEERS=1
         - PEERDNS=auto
       volumes:
         - ./config:/config
         - /lib/modules:/lib/modules
       ports:
         - 51820:51820/udp
       sysctls:
         - net.ipv4.conf.all.src_valid_mark=1
       restart: unless-stopped
   ```

   Replace `your-server-ip` with your server's public IP address.

2. **Launch the WireGuard Server**:

   Run the following command to start the server:

   ```bash
   docker-compose up -d
   ```

3. **Configure the Client**:

   After launching the container, check the configuration files in the `~/wireguard/config/etc/wireguard` directory. The `.conf` file created will be for the client; copy it to your device and use a compatible WireGuard app to connect.

#### 3.2 Setting Up OpenVPN

1. **Deploy OpenVPN using Docker**:

   Create a directory for OpenVPN configuration:

   ```bash
   mkdir ~/openvpn
   cd ~/openvpn
   ```

   Create a `docker-compose.yml` file:

   ```yaml
   version: '2'
   services:
     openvpn:
       image: kylemanna/openvpn
       container_name: openvpn
       cap_add:
         - NET_ADMIN
       volumes:
         - ./ovpn-data:/etc/openvpn
       ports:
         - 1194:1194/udp
       restart: unless-stopped
   ```

2. **Initialize the OpenVPN Server**:

   Initialize the PKI and set up a server:

   ```bash
   docker run --rm -v ~/openvpn/ovpn-data:/etc/openvpn --log-driver=none --cap-add=NET_ADMIN kylemanna/openvpn ovpn_genconfig -u udp://your-server-ip
   docker run --rm -v ~/openvpn/ovpn-data:/etc/openvpn -it kylemanna/openvpn ovpn_initpki
   ```

   Follow the prompts to complete the initialization.

3. **Create a Client Configuration**:

   Generate a client certificate and configuration:

   ```bash
   docker run --rm -v ~/openvpn/ovpn-data:/etc/openvpn -it kylemanna/openvpn easyrsa build-client-full CLIENTNAME nopass
   docker run --rm -v ~/openvpn/ovpn-data:/etc/openvpn kylemanna/openvpn ovpn_getclient CLIENTNAME > CLIENTNAME.ovpn
   ```

   Copy `CLIENTNAME.ovpn` to your client device and import it into your OpenVPN client application.

### 4. Manage DNS (Optional, using Cloudflare)

If you have a domain, it can be helpful to set up a DNS record for easier access. Using Cloudflare:

1. Log into Cloudflare and navigate to the DNS settings of your domain.
2. Add an "A" or "CNAME" record pointing to your server's IP.

### 5. Security and Firewall Configuration

Ensure your firewall settings allow traffic to your VPN ports:

```bash
ufw allow 51820/udp  # For WireGuard
ufw allow 1194/udp   # For OpenVPN
ufw enable
```

## Troubleshooting

1. **Connection Issues**:
   - Ensure that your server's public IP is correctly configured.
   - Verify port-forwarding if you're behind a NAT.

2. **Slow Connection Speeds**:
   - Check the server's resources and network bandwidth.
   - Ensure no bandwidth limit is configured on the VPN server.

3. **Client Errors**:
   - Check logs: `docker logs wireguard` or `docker logs openvpn` for errors.
   - Ensure client configuration matches server details.

## Conclusion

By following this tutorial, you now have a self-hosted VPN setup that grants you complete control over your virtual private network. Whether you chose WireGuard for its speed and simplicity or OpenVPN for its robustness, you've taken a significant step towards enhancing your online privacy. Remember, the security of your VPN largely depends on the practices you maintain. Keep your server updated and regularly review security configurations.

Self-hosting a VPN can be a rewarding experience, offering insight into networking technologies while enhancing your online security landscape. Enjoy safe browsing!