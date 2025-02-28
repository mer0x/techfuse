---
title: "How to self-hosted VPN with WireGuard"
date: "2025-02-28"
draft: false
toc: true
tags: []
categories: []
summary: "A complete guide on How to self-hosted VPN with WireGuard."
cover:
  image: "img/covers/how-to-self-hosted-vpn-with-wireguard.jpg"
  alt: "How to self-hosted VPN with WireGuard"
---
```markdown
---
title: "How to Self-host a VPN with WireGuard"
date: 2023-10-15
draft: false
toc: true
tags: [WireGuard, VPN, Self-hosting, Docker, Ansible, Security]
categories: [Networking, Security]
summary: "A detailed guide on how to self-host a VPN using WireGuard."
alt: "How to self-host a VPN with WireGuard"
---

# How to Self-host a VPN with WireGuard

Virtual Private Networks (VPNs) have become essential for secure and private communication over the internet. WireGuard, a modern, fast, and lightweight VPN protocol, offers a simple yet powerful way to achieve this. In this tutorial, we'll walk through the process of self-hosting a VPN using WireGuard, leveraging modern tools like Docker and Ansible.

## Introduction

WireGuard is known for its simplicity and performance. Unlike traditional VPN protocols like OpenVPN and IPSec, WireGuard is designed to be easy to configure, deploy, and manage. It uses state-of-the-art cryptography and provides a high-speed, low-latency connection, making it an excellent choice for a self-hosted VPN solution.

## Prerequisites

Before we start, make sure you have the following:

- A server with a public IP address to host the VPN (e.g., a VPS from DigitalOcean, AWS, etc.).
- Basic knowledge of Linux command line and networking concepts.
- Docker and Docker Compose installed on your server.
- Ansible installed on your local machine for automation.
- A domain name for easier access (optional but recommended).

## Step-by-step Guide

### Step 1: Setting Up Your Server

First, ensure your server is up to date:

```bash
sudo apt update && sudo apt upgrade -y
```

Install necessary packages:

```bash
sudo apt install -y wireguard-tools qrencode
```

### Step 2: Installing WireGuard

We'll use Docker to run WireGuard, which simplifies management and deployment.

#### Docker Setup

1. Create a directory for WireGuard:

   ```bash
   mkdir -p ~/wireguard && cd ~/wireguard
   ```

2. Create a `docker-compose.yml` file:

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
         - SERVERURL=your.domain.com # Replace with your domain
         - SERVERPORT=51820
         - PEERS=1 # Number of clients
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

3. Start the WireGuard container:

   ```bash
   docker-compose up -d
   ```

### Step 3: Configuring WireGuard

The configuration files are generated in the `config` directory. You can add additional peers by increasing the `PEERS` environment variable or manually editing the config files.

#### Accessing Configurations

To view the peer configuration, use:

```bash
cat ./config/peer1/peer1.conf
```

To connect a client, you can generate a QR code for mobile devices:

```bash
qrencode -t ansiutf8 < ./config/peer1/peer1.conf
```

### Step 4: Using Ansible for Automation

To automate the deployment across multiple servers or environments, use Ansible.

1. Install Ansible:

   ```bash
   sudo apt install ansible -y
   ```

2. Create an Ansible playbook `wireguard.yml`:

   ```yaml
   - hosts: wireguard_servers
     become: true
     tasks:
       - name: Ensure Docker is installed
         apt:
           name: docker.io
           state: present

       - name: Ensure Docker Compose is installed
         apt:
           name: docker-compose
           state: present

       - name: Deploy WireGuard with Docker
         copy:
           src: ./docker-compose.yml
           dest: /home/ubuntu/wireguard/docker-compose.yml
         notify:
           - Run WireGuard

     handlers:
       - name: Run WireGuard
         command: docker-compose up -d
         args:
           chdir: /home/ubuntu/wireguard
   ```

3. Define your inventory in `hosts.ini`:

   ```ini
   [wireguard_servers]
   your_server_ip ansible_ssh_user=ubuntu
   ```

4. Run the playbook:

   ```bash
   ansible-playbook -i hosts.ini wireguard.yml
   ```

## Security

WireGuard is secure by default, but there are additional steps you can take to harden your setup:

- **Firewall Rules**: Ensure that only necessary ports are open. Use UFW or iptables to restrict access.
  
  ```bash
  sudo ufw allow 51820/udp
  sudo ufw enable
  ```

- **Regular Updates**: Keep your server and Docker images updated to protect against vulnerabilities.
- **Encryption**: Always use strong, unique keys for peers.

## Troubleshooting

Here are common issues and solutions:

- **Cannot connect to the VPN**: Ensure the server's firewall allows UDP traffic on port 51820 and that your client configuration is correct.
- **Slow Speeds**: Check server load and network bandwidth. Ensure no throttling occurs on the server side.
- **Docker issues**: Restart Docker services if containers fail to start:

  ```bash
  sudo systemctl restart docker
  ```

## Conclusion

Self-hosting a VPN with WireGuard is a powerful way to secure your internet traffic with minimal overhead. By using Docker and Ansible, you can deploy and manage your VPN efficiently. With its strong security and performance benefits, WireGuard is an excellent choice for both personal and professional use.

By following this guide, you should now have a functional WireGuard VPN server. As always, continue to monitor and update your setup to ensure optimal performance and security.

Happy networking!
```