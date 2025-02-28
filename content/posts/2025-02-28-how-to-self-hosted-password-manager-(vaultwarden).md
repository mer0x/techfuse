---
title: "How to self-hosted password manager (Vaultwarden)"
date: 2025-02-28
tags: ["Self-Hosting", "DevOps", "Homelab", "Networking"]
categories: ["IT Tutorials"]
draft: false
---
# How to Self-Host Password Manager (Vaultwarden)

Password management is a fundamental aspect of modern digital security. Choosing to self-host a password manager can significantly enhance your security and give you full control over your data. Vaultwarden, formerly known as Bitwarden_RS, is a lightweight, self-hostable version of Bitwarden—one of the most popular open-source password managers. In this tutorial, we will guide you through setting up your instance of Vaultwarden using Docker and other popular tools like Proxmox, Ansible, and Cloudflare to fortify your password management infrastructure.

---

## Introduction

With the increase in online services requiring user accounts, managing a myriad of passwords has become cumbersome and risky. Self-hosting your password manager ensures that your sensitive information is under your control, eliminating dependency on third-party services and reducing potential exposure in case of data breaches. Vaultwarden offers an effective solution due to its lightweight nature and feature-rich design, providing all the necessary components to secure your passwords.

### Key Benefits of Self-Hosting Vaultwarden:

- **Data Ownership:** You hold the keys to your data, hence mitigating privacy risks.
- **Customizability:** Easily tailor the setup to your specific security needs.
- **Cost-Effective:** Eliminate subscription fees associated with third-party hosted services.
- **Flexible Deployment:** Can be run on multiple platforms such as Docker, Proxmox, or bare metal.

---

## Prerequisites

Before diving into the installation and configuration of Vaultwarden, ensure you have the following:

- **Basic Knowledge:** Understanding of Docker, Ansible, and Linux command line operations.
- **Server Environment:** A server running a modern Linux distribution (Debian/Ubuntu recommended).
- **Docker Installed:** Ensure Docker is installed and running on your server.
- **Domain Name:** A domain pointed to your server's IP for SSL setup.
- **Cloudflare Account:** Optional for DNS management and added security.
- **Proxmox VE:** Optional for virtualization management.

## Step-by-Step Implementation

### Step 1: Setting Up Docker Environment

1. **Update System Packages:**
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. **Install Docker:**
   Follow these commands to install Docker:
   ```bash
   sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
   curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
   sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
   sudo apt update
   sudo apt install -y docker-ce
   ```

3. **Verify Docker Installation:**
   ```bash
   docker --version
   ```

### Step 2: Deploying Vaultwarden with Docker

1. **Create Docker Network:**
   ```bash
   docker network create vaultwarden-net
   ```

2. **Start Vaultwarden Container:**
   Execute the following command to run a Vaultwarden instance.
   ```bash
   docker run -d --name vaultwarden \
     --network vaultwarden-net \
     -e WEBSOCKET_ENABLED=true \
     -v /vw-data:/data \
     -p 80:80 \
     --restart unless-stopped \
     vaultwarden/server:latest
   ```

3. **Enable HTTPS with Let's Encrypt:**
   Use a reverse proxy like Nginx or Traefik integrated with Let's Encrypt for SSL/TLS.
   - **Using Nginx:** Ensure your domain is set to point at your server and add an Nginx configuration with Certbot for SSL.

### Step 3: Setting Up Cloudflare

1. **Point Domain to Server:**
   - Log in to your Cloudflare account and add a DNS `A` record pointing your domain or subdomain to your server's IP.

2. **Enable Proxy Status:**
   - Enhance security by enabling Cloudflare's proxy, allowing Cloudflare to handle HTTPS connections.

### Step 4: Managing Infrastructure with Proxmox and Ansible

**Using Proxmox VE:**
- Install Proxmox on a physical server to manage your Docker environments efficiently.
  - Create a VM or LXC that runs your Docker instance for Vaultwarden.

**Using Ansible for Automation:**

1. **Set up Ansible in your control node:**
   ```bash
   sudo apt install -y ansible
   ```

2. **Write an Ansible Playbook for Vaultwarden:**
   Create a playbook for automated deployment. Below is a basic snippet for Docker setup:
   ```yaml
   - hosts: vaultwarden_host
     tasks:
       - name: Install Docker
         apt:
           name: docker-ce
           state: present
           update_cache: yes
       - name: Run Vaultwarden Container
         docker_container:
           name: vaultwarden
           image: vaultwarden/server:latest
           state: started
           restart_policy: unless-stopped
           network_mode: bridge
           volumes:
             - /vw-data:/data
   ```

### Step 5: Securing and Monitoring

- **Regular Backups:** Implement periodic backups of your `vw-data` directory storing your Vaultwarden data.
- **Monitoring:** Deploy monitoring tools like Grafana or Prometheus for enhanced observability.

---

## Troubleshooting

- **Container Not Starting:**
  - Check the Docker logs using `docker logs vaultwarden` for any error messages.
  
- **SSL Issues:**
  - Ensure your DNS records are correctly pointing to your server's IP and that the ports are open.
  
- **Access Issues:**
  - Double-check your firewall settings to ensure ports used by Vaultwarden (80/443) are open.

---

## Conclusion

Self-hosting Vaultwarden not only aids in keeping your passwords secure but also instills a sense of ownership and trust in the way your data is managed. By following this guide, you will have a robust password management system deployed and configured correctly using industry-standard tools such as Docker, Proxmox, and Cloudflare. Remember, continuous monitoring and updating software components are paramount in maintaining a secure environment. Enjoy the peace of mind that comes with keeping your credentials protected and entirely under your control.