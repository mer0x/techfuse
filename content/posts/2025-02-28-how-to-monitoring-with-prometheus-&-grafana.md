---
date: 2025-02-28

---

# How to Monitor with Prometheus & Grafana: A Comprehensive Self-Hosting Guide

Monitoring your infrastructure and applications is critical for maintaining system health and performance. Among the most popular tools for this purpose are Prometheus and Grafana, renowned for their robustness and flexibility in collecting and visualizing metrics. This tutorial will guide you on setting up Prometheus and Grafana for effective monitoring, ensuring you have insight into your systems' performance in real-time.

## Introduction

Modern infrastructure demands robust monitoring solutions that can gather and display metrics, providing actionable insights. Prometheus is an open-source tool designed for monitoring and alerting. It collects metrics from configured targets at given intervals, evaluates rule expressions, displays the results, and triggers alerts if any condition is met. Grafana, on the other hand, is widely used for visualizing time-series data. Combining Prometheus and Grafana offers a powerful self-hosting monitoring solution.

### Why Self-Host Prometheus and Grafana?

1. **Control over Data**: Self-hosting allows complete control over your data without relying on third-party services.
2. **Customization**: Tailor the installations to suit your specific monitoring needs and integrate seamlessly with existing infrastructure.
3. **Cost-Efficiency**: Reduces the need for subscription-based monitoring services.
4. **Security**: Control over security configurations, ensuring data privacy and compliance with any standards.

### Tools Overview

- **Prometheus**: Ideal for collecting and storing time-series data, with a powerful query language for accessing real-time data.
- **Grafana**: Best for creating dashboards from various data sources, offering beautiful and insightful visualizations.

## Prerequisites

Before implementing the monitoring solution, ensure you have the following:

1. **Docker & Docker Compose Installed**: For running containerized applications.
2. **Basic Understanding of Linux Commands**: As most steps require commandeering the server environment.
3. **Access to a Linux-based Server**: Ubuntu 20.04 LTS or later is recommended.
4. **Proxmox or Virtualization Infrastructure**: Optional, for resource allocation and managing virtual machines.
5. **Cloudflare Account**: Optional, for managing DNS and HTTPS for your hostnames.

## Step-by-Step Implementation

### Step 1: Setting up Docker & Docker Compose

Ensure Docker is installed on your Linux server. Follow these commands if Docker is not yet installed:

```bash
sudo apt update
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt update
sudo apt install -y docker-ce
```

Next, install Docker Compose:

```bash
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose --version
```

### Step 2: Deploying Prometheus

Create a directory to house your Prometheus files:

```bash
mkdir ~/prometheus
cd ~/prometheus
```

Create a `Dockerfile` and a configuration file `prometheus.yml` in the directory:

**Dockerfile:**

```dockerfile
FROM prom/prometheus
COPY prometheus.yml /etc/prometheus/
```

**prometheus.yml**:

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']
```

Deploy with Docker Compose by creating a `docker-compose.yml`:

```yaml
version: '3.7'

services:
  prometheus:
    build: .
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
```

Run the Docker containers:

```bash
docker-compose up -d
```

### Step 3: Deploying Grafana

Create a directory for Grafana:

```bash
mkdir ~/grafana
```

Create a `docker-compose.yml` file inside that directory as follows:

```yaml
version: '3.7'

services:
  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    volumes:
      - grafana-storage:/var/lib/grafana

volumes:
  grafana-storage:
```

Deploy Grafana using:

```bash
docker-compose up -d
```

### Step 4: Configuring Prometheus & Grafana

#### Access Prometheus

Visit `http://YOUR_SERVER_IP:9090` to verify Prometheus is running. You should see the Prometheus dashboard.

#### Connect Grafana to Prometheus

Navigate to `http://YOUR_SERVER_IP:3000` to access Grafana. Use the default credentials (`admin/admin`) to log in. Change your password when prompted.

- Go to `Configuration` -> `Data Sources`.
- Add a new data source and select `Prometheus`.
- Set the URL to `http://prometheus:9090`.
- Save and Test the connection.

#### Create Dashboards

- Once data source is configured, navigate to `Create` -> `Dashboard`.
- Use the `Panel` button to add Prometheus metrics and visualize them.
- Save your dashboard configurations.

### Step 5: Secure Access (Optional)

For securing access, configure Cloudflare DNS settings with your server's IP, and manage HTTPS using Cloudflare's SSL settings.

## Troubleshooting

- **Cannot Access Grafana/Prometheus Web UI**: Check if Docker services are running using `docker-compose ps`. Ensure necessary ports (3000, 9090) are open in firewall.
- **Configuration Errors**: Validate `prometheus.yml` using Prometheus configuration validator.
- **Grafana Data Source Connection Fails**: Double-check network settings and data source URL configuration.

## Conclusion

With Prometheus and Grafana successfully set up, you now have a powerful, efficient monitoring system capable of scaling with your infrastructure. Tailor this guide to further customize metrics and dashboards to suit your unique needs. By self-hosting, you ensure greater control and security over your monitoring data, all while maintaining cost-efficiency.

In an ever-evolving technological landscape, having real-time insights is invaluable. Leverage the power of Prometheus and Grafana to keep your systems healthy and performing optimally.

---