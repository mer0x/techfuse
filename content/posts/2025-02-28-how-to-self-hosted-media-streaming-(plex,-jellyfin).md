---
title: "How to self-hosted media streaming (Plex, Jellyfin)"
date: 2025-02-28
tags: ["Self-Hosting", "DevOps", "Homelab", "Networking"]
categories: ["IT Tutorials"]
draft: false
---
```markdown
---
title: "How to Self-Host Media Streaming with Plex and Jellyfin"
date: 2023-10-10
description: "A detailed tutorial on how to self-host your media streaming platform using Plex and Jellyfin, with Docker, Ansible, and Proxmox."
tags: ["Self-Hosting", "Media Streaming", "Plex", "Jellyfin", "Docker", "Ansible", "Proxmox", "Cloudflare"]
---

# Introduction

In an age where digital privacy is paramount, controlling your media streaming setup provides significant advantages. Self-hosting solutions like Plex and Jellyfin empower you to manage, control, and secure your media environment. This tutorial offers a comprehensive guide to help you set up your self-hosted media streaming service using top tools such as Docker, Ansible, Proxmox, and Cloudflare. Whether you're a privacy enthusiast or simply want unrestrained access to your media library, this guide will get you started.

## Why Self-Host Media Streaming?

Self-hosting media streaming services like Plex and Jellyfin grants you full control over your digital library. Here's why it's beneficial:

- **Privacy**: Store your media on hardware you control.
- **Customization**: Tailor your media server to suit your specific needs.
- **Cost efficiency**: Reduce dependency on subscription services.
- **Accessibility**: Stream your content from anywhere in the world.

## Prerequisites

Before diving into the setup, ensure you have the following:

1. **Hardware**: A machine with adequate storage and processing power.
2. **Operating System**: Ubuntu 20.04 LTS for ease of use and stability.
3. **Networking**: A stable internet connection.
4. **Domain**: A domain name (e.g., from Namecheap) for remote access.
5. **Proficiency**: Basic knowledge of Linux command-line, Docker, and networking.

## Step-by-Step Implementation

### Step 1: Setting Up Proxmox VE

1. **Install Proxmox VE**: Proxmox is a robust platform for managing virtualized environments.

    - Download the Proxmox VE ISO installer from [Proxmox's official website](https://www.proxmox.com/en/).
    - Follow the [installation guide](https://pve.proxmox.com/wiki/Installation) to install on your dedicated server.

2. **Create a VM**: Use Proxmox to create a Debian/Ubuntu virtual machine for hosting the media servers.

    ```bash
    # Create and configure a new VM
    qm create 100 --name Media-Server --memory 8096 --net0 virtio,bridge=vmbr0
    ```

### Step 2: Installing Docker

1. **Update Repositories and Install Dependencies**:

    ```bash
    sudo apt update
    sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
    ```

2. **Add Docker's GPG Key and Repository**:

    ```bash
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
    ```

3. **Install Docker**:

    ```bash
    sudo apt update
    sudo apt install -y docker-ce
    sudo systemctl start docker
    sudo systemctl enable docker
    ```

### Step 3: Deploying Plex and Jellyfin Containers

1. **Create a Docker Network**:

    ```bash
    docker network create media_net
    ```

2. **Deploy Plex Container**:

    ```bash
    docker run -d --name=plex --network=media_net --restart=unless-stopped -e PLEX_CLAIM="<your_claim_token>" -e ADVERTISE_IP="http://your-server-public-ip:32400/" -p 32400:32400 -p 3005:3005 -p 8324:8324 -p 32469:32469 -v /path/to/library:/media -v /plex-config:/config plexinc/pms-docker
    ```

3. **Deploy Jellyfin Container**:

    ```bash
    docker run -d --name=jellyfin --network=media_net --restart=unless-stopped -p 8096:8096 -p 8920:8920 -v /path/to/jellyfin/config:/config -v /path/to/jellyfin/cache:/cache -v /path/to/media:/media jellyfin/jellyfin
    ```

### Step 4: Configuring Cloudflare DNS for Remote Access

1. **Set up DNS**:
   
    - Go to your Cloudflare dashboard.
    - Add a DNS A record pointing to your Proxmox public IP address.

2. **Enable Proxy**:

    - Ensure the 'Proxy status' is 'Proxied' to protect your server's IP and enable HTTPS.

### Step 5: Automating with Ansible

1. **Install Ansible on your control node**:

    ```bash
    sudo apt update
    sudo apt install -y ansible
    ```

2. **Create Ansible Playbook for Docker**:

    ```yaml
    ---
    - hosts: media_servers
      become: yes
      tasks:
        - name: Install Docker
          apt:
            name: ['apt-transport-https', 'ca-certificates', 'curl', 'software-properties-common']
            state: present
            update_cache: yes

        - name: Add Docker GPG key
          apt_key:
            url: https://download.docker.com/linux/ubuntu/gpg
            state: present

        - name: Add Docker repository
          apt_repository:
            repo: "deb [arch=amd64] https://download.docker.com/linux/ubuntu {{ ansible_distribution_release }} stable"

        - name: Install Docker-ce
          apt:
            name: docker-ce
            state: present
            update_cache: yes
    ```

3. **Apply Playbook**:

    ```bash
    ansible-playbook -i hosts docker-playbook.yml
    ```

## Troubleshooting

- **Network Issues**: Ensure your firewall/port forwarding rules allow traffic through Plex and Jellyfin ports.
- **Server Errors**: Inspect Docker logs using `docker logs <container-name>` for additional insights.
- **DNS Resolution**: Confirm your domain and IP address settings on Cloudflare are correct.

## Conclusion

By following this guide, you can successfully set up a self-hosted media streaming platform using Plex and Jellyfin. Embracing privacy and customization, you now have a powerful toolset at your disposal to enjoy your media library without compromise. A self-hosted solution is not only more private but also incredibly flexible and cost-efficient. Enjoy streaming!

---
```

This tutorial provides a structured approach to setting up a self-hosted media streaming service, enabling both novices and seasoned administrators to deploy Plex and Jellyfin on their own infrastructure. Through detailed steps and explanations, you can confidently manage your digital media environment.