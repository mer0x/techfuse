---
title: "How to monitor your infrastructure with Prometheus and Grafana"
date: "2025-02-28"
draft: false
toc: true
tags: []
categories: []
summary: "A complete guide on How to monitor your infrastructure with Prometheus and Grafana."
cover:
  image: "img/covers/how-to-monitor-your-infrastructure-with-prometheus-and-grafana.jpg"
  alt: "How to monitor your infrastructure with Prometheus and Grafana"
---
```markdown
---
title: "How to monitor your infrastructure with Prometheus and Grafana"
date: 2023-10-15
draft: false
toc: true
tags: [monitoring, Prometheus, Grafana, infrastructure, DevOps, Docker, self-hosting]
categories: [DevOps, Monitoring]
summary: "A detailed guide on How to monitor your infrastructure with Prometheus and Grafana."
cover:
  image: "img/covers/how-to-monitor-your-infrastructure-with-prometheus-and-grafana.jpg"
  alt: "How to monitor your infrastructure with Prometheus and Grafana"
---

# How to Monitor Your Infrastructure with Prometheus and Grafana

Monitoring is a crucial component of managing any IT infrastructure. In this tutorial, we'll explore how to effectively monitor your infrastructure using Prometheus and Grafana. These tools are open-source, powerful, and widely used in the industry for monitoring and visualization.

## Introduction

In today's fast-paced digital environment, maintaining uptime and performance of IT infrastructure is critical. Prometheus, with its robust data collection capabilities, combined with Grafana's intuitive data visualization, provides a comprehensive solution for monitoring and alerting. This tutorial will guide you through setting up Prometheus and Grafana from scratch using Docker, along with best security practices and troubleshooting tips.

## Prerequisites

Before we begin, ensure you have the following:

- **A basic understanding of Docker**: Since we'll use Docker to deploy Prometheus and Grafana, familiarity with Docker commands will be helpful.
- **A server or local machine**: Ensure you have a server or a local machine with at least 2GB of RAM and 2 CPUs.
- **Docker and Docker Compose installed**: Follow the [official Docker documentation](https://docs.docker.com/get-docker/) for installation instructions.
- **Network access**: Ensure that your firewall settings allow access to the necessary ports (9090 for Prometheus and 3000 for Grafana).

## Step-by-step Guide

### Step 1: Setting Up Prometheus

1. **Create a Docker Network**: This will allow Prometheus and Grafana to communicate.

   ```bash
   docker network create monitoring
   ```

2. **Create a Prometheus Configuration File**: Save this file as `prometheus.yml`.

   ```yaml
   global:
     scrape_interval: 15s

   scrape_configs:
     - job_name: 'prometheus'
       static_configs:
         - targets: ['localhost:9090']
   ```

3. **Create a Docker Compose File**: Save the following as `docker-compose.yml`.

   ```yaml
   version: '3.7'

   services:
     prometheus:
       image: prom/prometheus
       volumes:
         - ./prometheus.yml:/etc/prometheus/prometheus.yml
       command:
         - '--config.file=/etc/prometheus/prometheus.yml'
       ports:
         - 9090:9090
       networks:
         - monitoring

   networks:
     monitoring:
       external: true
   ```

4. **Start Prometheus**: Run the following command to start Prometheus.

   ```bash
   docker-compose up -d
   ```

5. **Verify the Setup**: Access Prometheus by navigating to `http://localhost:9090`.

### Step 2: Setting Up Grafana

1. **Add Grafana to Docker Compose**: Update `docker-compose.yml` to include Grafana.

   ```yaml
   services:
     grafana:
       image: grafana/grafana
       ports:
         - 3000:3000
       networks:
         - monitoring
   ```

2. **Start Grafana**: Run the following command to start Grafana.

   ```bash
   docker-compose up -d
   ```

3. **Access Grafana**: Navigate to `http://localhost:3000`. Use the default login credentials (`admin/admin`).

4. **Add Prometheus as a Data Source**:

   - Navigate to **Configuration > Data Sources** in the Grafana UI.
   - Click **Add data source**.
   - Choose **Prometheus** from the list.
   - Set the URL to `http://prometheus:9090`.
   - Click **Save & Test**.

5. **Create a Dashboard**: Explore Grafana's dashboard creation tools to visualize your data.

### Step 3: Adding Exporters

To monitor various services, you'll need exporters that expose metrics in a format Prometheus can understand.

1. **Node Exporter for System Metrics**:

   ```yaml
   services:
     node_exporter:
       image: prom/node-exporter
       ports:
         - 9100:9100
       networks:
         - monitoring
   ```

2. **Update Prometheus Configuration**: Add the node exporter to `prometheus.yml`.

   ```yaml
   scrape_configs:
     - job_name: 'node_exporter'
       static_configs:
         - targets: ['node_exporter:9100']
   ```

3. **Restart Services**:

   ```bash
   docker-compose down
   docker-compose up -d
   ```

## Security

### Securing Prometheus and Grafana

1. **Enable Authentication in Grafana**: Change the default admin password after the first login.
2. **Secure with HTTPS**: Use a reverse proxy like Nginx to add SSL to your setup.
3. **Network Security**: Use firewalls to restrict access to Prometheus and Grafana only to trusted IPs.

### Example Nginx Configuration

```nginx
server {
    listen 443 ssl;
    server_name your_domain;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    ssl_certificate /etc/ssl/certs/your_cert.crt;
    ssl_certificate_key /etc/ssl/private/your_cert.key;
}
```

## Troubleshooting

- **Prometheus Not Scraping Metrics**: Check if the Prometheus server can reach the target endpoints. Verify network connectivity and firewall rules.
- **Grafana Dashboard Issues**: Ensure the Prometheus data source is correctly configured and reachable.
- **Docker Issues**: Use `docker-compose logs` to diagnose any container-related problems.

## Conclusion

By following this tutorial, you should now have a fully functional monitoring setup using Prometheus and Grafana. This setup can be expanded with additional exporters and dashboards to monitor various aspects of your infrastructure. Remember to keep your systems secure and regularly update your Docker images to the latest versions.

Monitoring is not just about collecting data but also about understanding trends and anomalies. With Prometheus and Grafana in place, you're well-equipped to gain insights into your infrastructure's performance and reliability.

Feel free to explore the extensive plugins and community dashboards available for Grafana to further enhance your monitoring capabilities.

Happy Monitoring!
```