---
date: 2025-02-28

# Self-Hosting Media Streaming: A Comprehensive Guide to Plex and Jellyfin

In the age of streaming services, self-hosting your media server offers numerous advantages, such as complete control over your data, costs savings on subscription fees, and customizability. Among the popular self-hosting tools are Plex and Jellyfin, both of which offer robust media management capabilities. This tutorial guides you through the process of self-hosting a media server using Plex and Jellyfin, ensuring a seamless streaming experience.

## Prerequisites

Before diving into the implementation, ensure you have the following prerequisites covered:

- Basic knowledge of Linux command line operations.
- An up-to-date Linux server (Ubuntu 20.04 LTS or similar).
- Docker and Docker Compose installed.
- A domain name for accessing your server.
- A Cloudflare account for managing DNS if needed.
- Optional: A virtualization tool like Proxmox if you prefer to use VMs for segregation.

## Step-by-Step Implementation

### Step 1: Prepare Your Server Environment

#### Update and Upgrade Your Server

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl
```

#### Install Docker

To install Docker, use the following command:

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

Log out and log back in for group changes to take effect.

#### Install Docker Compose

Install Docker Compose using the following command:

```bash
sudo curl -L "https://github.com/docker/compose/releases/download/2.3.3/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

Verify the installation:

```bash
docker-compose --version
```

### Step 2: Setup Plex Media Server

#### Create a Docker Compose File

Create a directory for Plex and navigate into it.

```bash
mkdir ~/plex && cd ~/plex
```

Create a `docker-compose.yml` file with the following content:

```yaml
version: '3.8'
services:
  plex:
    image: lscr.io/linuxserver/plex
    container_name: plex
    environment:
      - PUID=1000
      - PGID=1000
      - VERSION=docker
      - PLEX_CLAIM=yourClaimToken # Optional - for sign in
    volumes:
      - /path/to/library/config:/config
      - /path/to/library/tvshows:/data/tvshows
      - /path/to/library/movies:/data/movies
    network_mode: host
    restart: unless-stopped
```

Replace the `/path/to/library` paths with actual paths on your server. Obtain a `PLEX_CLAIM` token from [Plex website](https://plex.tv/claim) for easier setup.

#### Deploy Plex

Run the docker-compose command to start Plex:

```bash
docker-compose up -d
```

### Step 3: Setup Jellyfin Media Server

#### Create a Docker Compose File for Jellyfin

Create a directory for Jellyfin and navigate into it.

```bash
mkdir ~/jellyfin && cd ~/jellyfin
```

Create a `docker-compose.yml` file with the following content:

```yaml
version: '3.8'
services:
  jellyfin:
    image: jellyfin/jellyfin
    container_name: jellyfin
    volumes:
      - /path/to/config:/config
      - /path/to/cache:/cache
      - /path/to/library/tvshows:/data/tvshows
      - /path/to/library/movies:/data/movies
    ports:
      - 8096:8096
    restart: unless-stopped
```

Replace the `/path/to/library` paths with actual paths on your server.

#### Deploy Jellyfin

Run the docker-compose command to start Jellyfin:

```bash
docker-compose up -d
```

### Step 4: Configure Access Through Cloudflare

If you wish to access your media server externally using a domain name:

1. Set up a subdomain for your home server in your domain's DNS settings, pointing to your public IP.
2. Use a proxy service like Cloudflare for added security:
   - Add a DNS entry in Cloudflare for `plex.yourdomain.com` and `jellyfin.yourdomain.com`, both pointed to your server's public IP.
   - Enable "Proxy Status" to provide additional DDoS protection.

### Step 5: Proxmox Virtualization (Optional)

If using Proxmox to manage virtual environments, follow these steps:

1. Create a new VM for each media server and install the appropriate Linux distribution.
2. Follow the Docker and Docker Compose installation instructions within each VM.

## Troubleshooting

### Common Issues

1. **Port Conflicts**: Ensure there are no port conflicts. Change the host ports in `docker-compose.yml` if needed.
2. **Permissions**: Ensure the user running Docker has permissions to access the media directories.
3. **Firewall Rules**: Open ports 32400 (Plex) and 8096 (Jellyfin) on your firewall if you cannot access the services.

### Debugging

To check the logs and see detailed error messages, use:

```bash
docker logs plex
docker logs jellyfin
```

## Conclusion

Setting up a self-hosted media streaming server using Plex and Jellyfin can significantly enhance your media consumption experience while providing unprecedented control and cost savings. By leveraging Docker and optionally Proxmox, you can ensure your setup is scalable, manageable, and secure. Whether you're streaming to your living room or abroad, following these instructions will make sure you're never far from your media. Enjoy the capabilities of your self-hosted media server!

---