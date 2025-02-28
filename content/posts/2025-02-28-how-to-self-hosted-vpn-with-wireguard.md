---
categories: []
cover:
  alt: How to self-hosted VPN with WireGuard
  image: img/covers/how-to-self-hosted-vpn-with-wireguard.jpg
date: '2025-02-28'
draft: false
summary: A complete guide on How to self-hosted VPN with WireGuard.
tags: []
title: How to self-hosted VPN with WireGuard
toc: true
---

```markdown
---
title: "How to Self-Hosted VPN with WireGuard"
date: {{ .Date }}
draft: false
toc: true
tags: 
  - VPN
  - WireGuard
  - Self-hosting
  - Networking
  - Docker
  - Ansible
  - Security
categories: 
  - Networking
summary: Learn how to set up a self-hosted VPN using WireGuard with real-world tested code examples using Docker, Ansible, and bash scripts.
cover:
  image: "img/covers/how-to-self-hosted-vpn-with-wireguard.jpg"
  alt: "How to self-hosted VPN with WireGuard"
---

## Introduction

In today's digital world, security and privacy are paramount. One effective way to enhance your online security is by using a Virtual Private Network (VPN). WireGuard is a modern, open-source VPN solution known for its simplicity, speed, and robust encryption. This guide will walk you through setting up a self-hosted VPN using WireGuard, with hands-on examples using Docker, Ansible, and bash scripts. By the end of this tutorial, you'll have a fully operational VPN that you control.

## Prerequisites

Before diving into the implementation, ensure you have the following:

- A basic understanding of networking concepts.
- A server with a public IP address (e.g., a VPS).
- SSH access to the server.
- Docker and Docker Compose installed on your server.
- Ansible installed on your local machine.
- Basic knowledge of command-line operations.

## Step-by-Step Implementation

### Setting Up the Environment

First, we need to prepare our server environment. We'll use Docker to containerize our WireGuard setup.

#### Install Docker on the Server

```bash
sudo apt update
sudo apt install -y docker.io
sudo systemctl enable --now docker
```

#### Install Docker Compose

```bash
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### Using Docker to Deploy WireGuard

Create a directory for your WireGuard setup and navigate into it:

```bash
mkdir ~/wireguard-vpn && cd ~/wireguard-vpn
```

Create a `docker-compose.yml` file:

```yaml
version: '3.8'

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
      - PEERS=3
      - PEERDNS=auto
      - INTERNAL_SUBNET=10.13.13.0
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

Start the Docker container:

```bash
docker-compose up -d
```

### Using Ansible for Configuration Management

Create an Ansible playbook to automate the configuration:

```yaml
---
- hosts: wireguard
  become: true
  tasks:
    - name: Ensure Docker is installed
      apt:
        name: docker.io
        state: present

    - name: Ensure Docker Compose is installed
      get_url:
        url: https://github.com/docker/compose/releases/download/1.29.2/docker-compose-{{ ansible_system | lower }}-{{ ansible_architecture }}
        dest: /usr/local/bin/docker-compose
        mode: '0755'
```

Run your playbook:

```bash
ansible-playbook -i inventory.ini wireguard.yml
```

## Configuration and Customization

Once the WireGuard server is running, you can customize your VPN settings.

### Generate Client Configurations

Access the configuration directory:

```bash
cd ~/wireguard-vpn/config/peer*
```

Each peer directory will contain a `peer*.conf` file. This is your client's configuration file, which you can import into any WireGuard client app.

### Adjusting WireGuard Settings

Modify the `docker-compose.yml` file to change settings like the number of peers, DNS settings, or internal subnet.

## Security Considerations

- **Firewall Configuration:** Ensure that your server's firewall allows traffic on UDP port 51820.
  
  ```bash
  sudo ufw allow 51820/udp
  ```

- **Keep Software Updated:** Regularly update Docker, WireGuard, and your server to protect against vulnerabilities.

- **Use Strong Encryption:** Stick with WireGuard's default encryption settings, which are designed for optimal security.

## Troubleshooting

- **Connectivity Issues:** Check your server's firewall and ensure WireGuard is running.
- **Configuration Errors:** Verify your `docker-compose.yml` and client configuration files for typos or incorrect settings.
- **Log Analysis:** Use logs to diagnose issues. Access WireGuard logs via Docker:

  ```bash
  docker logs wireguard
  ```

## Conclusion

Setting up a self-hosted VPN with WireGuard is an excellent way to enhance your online privacy and security. With Docker and Ansible, the deployment and management process becomes streamlined and efficient. This guide provided you with a foundation to start your journey towards self-hosting a VPN. Remember, the key to a secure VPN is keeping your system updated and regularly reviewing your security settings.

By following the steps outlined in this guide, you now have a reliable and efficient VPN solution tailored to your needs. Happy surfing!

```