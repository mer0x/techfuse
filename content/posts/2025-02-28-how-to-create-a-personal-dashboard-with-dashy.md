```markdown
---
draft: false
title: "How to create a personal dashboard with Dashy"
date: "2025-02-28"
false
toc: true
tags: [Dashy, Personal Dashboard, Self-Hosting, Docker, DevOps, Ansible, Bash Scripting]
categories: [DevOps, Self-Hosting]
summary: "Learn how to create a personalized dashboard with Dashy, a flexible and customizable tool that allows you to manage and monitor your services efficiently."
cover:
    image: "img/covers/create-a-personal-dashboard-with-dashy.jpg"
    alt: "How to create a personal dashboard with Dashy"
---
draft: false
## Introduction

In today's digital age, managing multiple services and applications can be overwhelming. Having a centralized dashboard to monitor and control these services is not just a luxury but a necessity. This is where Dashy comes into play. Dashy is a self-hosted, highly customizable dashboard that allows you to organize and visualize your personal or professional tools in one place. Whether you're a DevOps engineer or a hobbyist, Dashy offers an intuitive interface to streamline your workflow and boost productivity. In this tutorial, we'll guide you through the process of setting up your personal dashboard using Dashy, leveraging tools like Docker and Ansible to ensure a smooth deployment.

## Prerequisites

Before you begin, ensure you have the following:

- **Hardware**: A server or a computer with at least 2GB of RAM and a dual-core CPU.
- **Software**:
  - Docker and Docker Compose installed on your system.
  - Basic understanding of command-line interface (CLI) operations.
  - Text editor (e.g., Visual Studio Code, Sublime Text).
  - Ansible installed (optional for automation).

## Step-by-Step Implementation

### Step 1: Setting Up Your Environment

First, ensure Docker is installed on your machine. You can verify the installation by running:

```bash
docker --version
```

If Docker is not installed, follow the [official installation guide](https://docs.docker.com/get-docker/).

### Step 2: Deploying Dashy with Docker

Create a directory for your Dashy project:

```bash
mkdir ~/dashy-dashboard
cd ~/dashy-dashboard
```

Create a `docker-compose.yml` file with the following content:

```yaml
version: '3.8'
services:
  dashy:
    image: lissy93/dashy:latest
    container_name: dashy
    ports:
      - "8080:80"
    volumes:
      - ./config.yml:/app/public/conf.yml
    restart: unless-stopped
```

This configuration pulls the latest Dashy image and maps port 8080 on your host to port 80 on the container.

### Step 3: Launching Dashy

Start the Dashy service with Docker Compose:

```bash
docker-compose up -d
```

Verify that Dashy is running by visiting `http://localhost:8080` in your web browser. You should see the default Dashy dashboard interface.

## Configuration and Customization

Dashy is highly customizable, allowing you to tailor the dashboard to your needs. The `config.yml` file is where you'll define your dashboard settings.

Create a basic `config.yml` file:

```yaml
title: "My Personal Dashboard"
appConfig:
  theme: navy
  layout: auto
  hideNavbar: false
  auth:
    enabled: false
sections:
  - name: "Productivity"
    items:
      - title: "Google"
        icon: "mdi-google"
        url: "https://www.google.com"
      - title: "GitHub"
        icon: "mdi-github"
        url: "https://github.com"
```

Edit this file to add or remove sections and items as per your requirements.

### Customizing Appearance

Dashy supports various themes and layout options. Modify the `theme` and `layout` fields in `config.yml` to change the appearance. Explore the [Dashy documentation](https://dashy.to/docs) for more customization options.

## Security Considerations

Security is paramount, especially when exposing services to the internet.

- **Authentication**: Enable basic authentication by setting `auth.enabled: true` in `config.yml`.
- **HTTPS**: If you're exposing Dashy externally, consider setting up a reverse proxy with Nginx or Traefik to enable HTTPS.
- **Firewall**: Configure your firewall to restrict access to the Dashy port.

## Troubleshooting Common Issues

### Issue 1: Dashy Container Fails to Start

Ensure no other services are using port 8080. Change the host port in `docker-compose.yml` if needed.

### Issue 2: Configuration Changes Not Reflecting

After editing `config.yml`, restart the Dashy container:

```bash
docker-compose restart dashy
```

### Issue 3: Access Denied Errors

Verify permissions on the `config.yml` file and ensure Docker has access to the directory.

## Conclusion and Next Steps

Congratulations on setting up your personal dashboard with Dashy! You've taken a significant step towards efficient service management. As next steps, consider automating the deployment with Ansible, integrating additional services, and exploring Dashy's advanced features like widget support and API integrations. The possibilities are endless!

With Dashy, you have a robust platform that grows with your needs, ensuring you stay organized and productive.

---
draft: false
By following this tutorial, you've equipped yourself with the skills to deploy and customize a Dashy dashboard, paving the way for a more organized and efficient digital workspace. Happy dashboarding!
```