---
title: "How to self-host nextcloud securely"
date: "2025-02-28T16:02:55.823089"
tags: ["Self-Hosting", "DevOps", "Homelab", "Networking"]
categories: ["IT Tutorials"]
draft: false
---
## Introduction

Self-hosting Nextcloud offers a personal or organizational solution to manage and share files, calendars, contacts, and more. By taking control of sensitive data, you avoid third-party cloud storage risks, ensuring compliance with data protection regulations. Nextcloud offers extensive features and is supported by a vibrant community making it an ideal choice for self-hosting. This tutorial will guide you through securely self-hosting Nextcloud using Docker, leveraging tools like Nginx for web servers, Let's Encrypt for free SSL/TLS certificates, and fail2ban for intrusion prevention.

## Prerequisites

- **Basic knowledge of Linux:** Comfort with command-line operations is necessary.
- **A Linux server:** Ubuntu Server 22.04 or newer recommended.
- **Docker and Docker Compose:** Installed and configured on your system.
- **Domain Name:** Ensure you have a registered domain that can be pointed to your server.
- **Firewall:** Ensure a firewall is set up, allowing ports 80, 443, and SSH.

## Step-by-Step Implementation

### Step 1: Setup Your Server Environment

1. **Update and Upgrade Your System:**

   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. **Install Docker and Docker Compose:**

   Follow official instructions to [install Docker](https://docs.docker.com/engine/install/ubuntu/) for Ubuntu:
   
   ```bash
   sudo apt install docker.io -y
   sudo systemctl enable --now docker
   ```

   To install Docker Compose:

   ```bash
   sudo apt install docker-compose -y
   ```

3. **Set up a Non-Root User:**

   Create a dedicated user with sudo privileges:

   ```bash
   sudo adduser nextcloud
   sudo usermod -aG sudo,docker nextcloud
   ```

4. **Configure Firewall:**

   Using UFW to open necessary ports:

   ```bash
   sudo ufw allow OpenSSH
   sudo ufw allow 'Nginx Full'
   sudo ufw enable
   ```

### Step 2: Setup Nextcloud with Docker Compose

1. **Create Docker Compose File:**

   Create a directory for Nextcloud setup and create a `docker-compose.yml` file:

   ```bash
   mkdir ~/nextcloud && cd ~/nextcloud
   ```

   ```yaml
   version: '3.7'
   services:
     nextcloud:
       image: nextcloud:latest
       restart: unless-stopped
       ports:
         - 8080:80
       volumes:
         - nextcloud-data:/var/www/html
       environment:
         - MYSQL_PASSWORD=yourpassword
         - MYSQL_DATABASE=nextcloud
         - MYSQL_USER=nextcloud
         - MYSQL_HOST=db

     db:
       image: mariadb
       restart: unless-stopped
       volumes:
         - db-data:/var/lib/mysql
       environment:
         - MYSQL_ROOT_PASSWORD=yourpassword
         - MYSQL_DATABASE=nextcloud
         - MYSQL_USER=nextcloud
         - MYSQL_PASSWORD=yourpassword

   volumes:
     nextcloud-data:
     db-data:
   ```

   Ensure to replace `yourpassword` with a strong password.

2. **Start the Docker Containers:**

   Execute the following command to start services:

   ```bash
   sudo docker-compose up -d
   ```

### Step 3: Secure Nextcloud with HTTPS

1. **Install Certbot for SSL Certificates:**

   Install Certbot and the Nginx plugin:

   ```bash
   sudo apt install certbot python3-certbot-nginx -y
   ```

2. **Get SSL Certificate:**

   Request SSL certificate for your domain:

   ```bash
   sudo certbot --nginx -d example.com -d www.example.com
   ```

3. **Set up Automatic Certificate Renewal:**

   Test the renewal process:

   ```bash
   sudo certbot renew --dry-run
   ```

### Step 4: Enhance Security with fail2ban

1. **Install fail2ban:**

   ```bash
   sudo apt install fail2ban -y
   ```

2. **Configure fail2ban for Nextcloud:**

   Create a custom filter:

   ```bash
   sudo nano /etc/fail2ban/jail.local
   ```

   Add the following configuration:

   ```
   [nextcloud]
   enabled = true
   filter = nextcloud
   port  = http,https
   logpath = /var/www/nextcloud-data/nextcloud.log
   maxretry = 3
   ```

   Ensure fail2ban is running:

   ```bash
   sudo systemctl enable --now fail2ban
   ```

### Troubleshooting

- **Nextcloud Setup Not Loading:**

  Ensure that Docker containers are running smoothly. Execute:

  ```bash
  sudo docker ps
  ```

  Check logs for errors:

  ```bash
  sudo docker-compose logs
  ```

- **SSL Certificate Issues:**

  Check Nginx configurations and ensure your domain DNS records point to your server. Re-run Certbot if needed.

- **Permissions Error:**

  Ensure Docker volumes are set correctly and check permissions of `/var/www/html`.

  ```bash
  sudo chown -R www-data:www-data /var/www/html
  ```

### Conclusion

Congratulations on setting up a secure, self-hosted Nextcloud instance! Through this guide, you have successfully deployed Nextcloud using Docker, secured it with Let's Encrypt, and protected it with fail2ban. You now possess control over your data ensuring privacy and compliance with data protection mandates.

For continuous smooth operations, consider setting up regular backups and monitor server performance. Explore Nextcloud’s apps and community forums for additional features and support.

## Tags

- Self-Hosting
- Nextcloud
- Docker
- Security
- Data Privacy
- SSL
- Linux
- Nginx
- fail2ban

Remember, the specifics might vary based on your server setup and configurations. Always tailor configurations to fit your security requirements best. Enjoy the sovereignty of your data with Nextcloud!