---
date: 2025-02-28

```markdown
---
title: "How to Self-Host a Media Streaming Service with Plex and Jellyfin"
date: 2023-10-10
description: "Detailed tutorial on self-hosting media streaming platforms like Plex and Jellyfin using Docker, Ansible, and more."
categories: ["DevOps", "Self-Hosting"]
tags: ["Plex", "Jellyfin", "Docker", "Proxmox", "Ansible", "Cloudflare"]
---

# How to Self-Host a Media Streaming Service with Plex and Jellyfin

## Introduction

In the age of digital consumption, media streaming platforms like Netflix, Amazon Prime, and Hulu have become household staples. However, they often come with limitations like restricted media libraries, subscription fees, and privacy concerns. This is where self-hosting your media streaming service using Plex or Jellyfin becomes an attractive alternative. Self-hosting provides complete control over your media library, ensuring privacy and limitless access to your movies, TV shows, and music.

### Why Self-Host Media Streaming?

1. **Privacy Control**: Keep your viewing habits and personal data out of third-party hands.
2. **Cost Efficiency**: Avoid recurring subscription fees of commercial platforms.
3. **Customizability**: Tailor features and configurations to your liking.
4. **Unlimited Library**: Host all your media without storage restrictions.

### Best Tools for Self-Hosting

- **Plex**: A popular media server that makes it easy to organize and stream your personal media.
- **Jellyfin**: An open-source alternative to Plex, offering privacy without subscriptions.
- **Docker**: Simplifies deployment and management of Plex/Jellyfin through containerization.
- **Ansible**: Automates server setup and application deployment.
- **Proxmox**: A virtualization solution for managing container and VM deployments.
- **Cloudflare**: Enhances security and performance for remote access, including a dynamic DNS solution.

## Prerequisites

- **Basic Understanding of Networking and Linux**: Essential for managing server setups and configurations.
- **Access to a Server or NAS**: Can be a home server, VPS, or a dedicated machine such as a Synology NAS.
- **Domain Name**: For accessing your service remotely.
- **Cloudflare Account**: Recommended for handling DNS and providing secure access.
- **Docker & Docker-Compose**: Installed on the server to simplify application deployment.

## Step-by-Step Implementation

### Step 1: Set Up Your Server or NAS

It's imperative to have a reliable server for hosting your media. Install a Linux distribution such as Ubuntu Server or CentOS. On a NAS, ensure that Docker is supported.

### Step 2: Set Up Docker and Docker-Compose

Install Docker and Docker-Compose on your Ubuntu server using:

```bash
sudo apt update
sudo apt install docker.io docker-compose
sudo systemctl start docker
sudo systemctl enable docker
```

### Step 3: Deploy Plex Using Docker

Create a directory for Docker configurations:

```bash
mkdir -p ~/docker/plex
```

Create a `docker-compose.yml` file:

```yaml
version: "3.8"
services:
  plex:
    image: plexinc/pms-docker
    container_name: plex
    network_mode: host
    environment:
      - PLEX_CLAIM=YOUR_PLEX_CLAIM
    volumes:
      - /path/to/plex/config:/config
      - /path/to/plex/transcode:/transcode
      - /path/to/media:/media
    restart: unless-stopped
```

Run the Docker container:

```bash
cd ~/docker/plex
docker-compose up -d
```

Access Plex via `http://<YOUR_SERVER_IP>:32400/web`.

### Step 4: Deploy Jellyfin Using Docker

Create a directory for Jellyfin:

```bash
mkdir -p ~/docker/jellyfin
```

Create a `docker-compose.yml` file for Jellyfin:

```yaml
version: '3.8'
services:
  jellyfin:
    image: jellyfin/jellyfin
    container_name: jellyfin
    network_mode: host
    volumes:
      - /path/to/jellyfin/config:/config
      - /path/to/jellyfin/cache:/cache
      - /path/to/media:/media
    restart: unless-stopped
```

Run the Jellyfin container:

```bash
cd ~/docker/jellyfin
docker-compose up -d
```

Access Jellyfin via `http://<YOUR_SERVER_IP>:8096`.

### Step 5: Use Ansible for Automation

Create an Ansible playbook for setting up media services:

```yaml
---
- name: Setup Media Server
  hosts: media_server
  become: yes
  tasks:
    - name: Install Docker
      apt: name=docker.io state=present update_cache=yes

    - name: Install Docker-Compose
      apt: name=docker-compose state=present

    - name: Deploy Plex
      docker_container:
        name: plex
        image: plexinc/pms-docker
        state: started
        restart_policy: unless-stopped
        volumes:
          - /path/to/plex/config:/config
          - /path/to/media:/media
        network_mode: host

    - name: Deploy Jellyfin
      docker_container:
        name: jellyfin
        image: jellyfin/jellyfin
        state: started
        restart_policy: unless-stopped
        volumes:
          - /path/to/jellyfin/config:/config
          - /path/to/media:/media
        network_mode: host
```

Run the playbook:

```bash
ansible-playbook -i inventory setup_media_server.yml
```

### Step 6: Configure Cloudflare for Secure Access

- Configure your DNS settings in Cloudflare to point your domain to your server's IP.
- Enable proxy and SSL settings to enhance security.

## Troubleshooting

### Common Issues

- **Ports Unavailable**: Ensure no other service is using the required ports (e.g., 32400 for Plex).
- **Permission Errors**: Validate that the Docker user has read/write permissions to the media directories.
- **Network Issues**: Verify Docker is running in host mode or configure attached network settings appropriately.

### Logs and Diagnostics

- Inspect Docker container logs using `docker logs <container_name>`.
- Check Docker and system service status with `systemctl status docker`.

## Conclusion

By following the steps outlined in this guide, you have equipped yourself with the knowledge and tools to self-host a full-fledged media streaming service using Plex and Jellyfin. With proper configuration, you can enjoy seamless and secure access to your personal media library. The tools and solutions described here provide a robust framework, ensuring that your setup is both reliable and scalable. Whether you're looking to reclaim privacy, cut costs, or relish in the personal satisfaction of managing your media, self-hosting provides these incredible benefits and more.

---

Embrace the empowerment that comes with self-hosting, and explore the boundless possibilities of your personalized media server!
```