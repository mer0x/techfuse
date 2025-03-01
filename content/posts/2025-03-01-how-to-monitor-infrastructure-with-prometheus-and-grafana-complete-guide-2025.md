---
title: "How to monitor infrastructure with Prometheus and Grafana - Complete Guide 2025"
date: 2025-03-01
draft: false
toc: true
tags: ["Monitor", "Infrastructure", "Prometheus", "Grafana", "Complete"]
categories: ["Infrastructure", "Automation"]
summary: "A comprehensive guide on How to monitor infrastructure with Prometheus and Grafana - Complete Guide 2025."
---

# How to Monitor Infrastructure with Prometheus and Grafana - Complete Guide 2025

In today's fast-paced digital landscape, real-time monitoring of infrastructure is crucial for maintaining robust and reliable services. Prometheus and Grafana have become the go-to tools for monitoring and visualization. This guide will walk you through everything you need to know to get started with infrastructure monitoring using these powerful tools.

## Introduction

Prometheus is an open-source monitoring and alerting toolkit designed for reliability and scalability. It collects metrics from configured targets at given intervals, evaluates rule expressions, displays results, and can trigger alerts if specified conditions arise. Grafana, on the other hand, is an open-source visualization and analytics software that provides a rich interface to create, explore, and share dashboards.

In this guide, we will cover setting up Prometheus, configuring it to scrape metrics, integrating it with Grafana, and creating dashboards to visualize your data. 

## Prerequisites

Before diving into the setup process, ensure that you have the following:

- A server or virtual machine with a modern Linux distribution (e.g., Ubuntu 22.04 or CentOS 9).
- Basic knowledge of Linux command-line operations.
- Docker installed on your machine (for containerized deployment).
- Internet access to download software packages.

## Step-by-step Guide

### Step 1: Installing Prometheus

1. **Download Prometheus:**

   ```bash
   wget https://github.com/prometheus/prometheus/releases/download/v2.45.0/prometheus-2.45.0.linux-amd64.tar.gz
   tar xvfz prometheus-2.45.0.linux-amd64.tar.gz
   cd prometheus-2.45.0.linux-amd64
   ```

2. **Configure Prometheus:**

   Edit the `prometheus.yml` file to define your scrape targets:

   ```yaml
   global:
     scrape_interval: 15s
     evaluation_interval: 15s

   scrape_configs:
     - job_name: 'node'
       static_configs:
         - targets: ['localhost:9100']
   ```

3. **Run Prometheus:**

   Start Prometheus using the following command:

   ```bash
   ./prometheus --config.file=prometheus.yml
   ```

   Prometheus will be accessible at `http://localhost:9090`.

### Step 2: Installing Node Exporter

Node Exporter is a Prometheus exporter for hardware and OS metrics.

1. **Download and Install Node Exporter:**

   ```bash
   wget https://github.com/prometheus/node_exporter/releases/download/v1.6.0/node_exporter-1.6.0.linux-amd64.tar.gz
   tar xvfz node_exporter-1.6.0.linux-amd64.tar.gz
   cd node_exporter-1.6.0.linux-amd64
   ```

2. **Run Node Exporter:**

   ```bash
   ./node_exporter
   ```

   Node Exporter will be accessible at `http://localhost:9100`.

### Step 3: Installing Grafana

1. **Download and Install Grafana:**

   Use Docker for a quick setup:

   ```bash
   docker run -d -p 3000:3000 --name=grafana grafana/grafana
   ```

   Alternatively, install Grafana using a package manager:

   ```bash
   sudo apt-get install -y apt-transport-https
   sudo apt-get install -y software-properties-common wget
   wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
   sudo add-apt-repository "deb https://packages.grafana.com/oss/deb stable main"
   sudo apt-get update
   sudo apt-get install grafana
   sudo systemctl start grafana-server
   sudo systemctl enable grafana-server
   ```

   Grafana will be accessible at `http://localhost:3000`.

### Step 4: Integrate Prometheus with Grafana

1. **Login to Grafana:**

   Open your browser and go to `http://localhost:3000`. The default login credentials are `admin` for both username and password. Change the password when prompted.

2. **Add Prometheus as a Data Source:**

   - Navigate to **Configuration** > **Data Sources** > **Add data source**.
   - Select **Prometheus**.
   - Enter `http://localhost:9090` in the URL field.
   - Click **Save & Test** to verify the connection.

### Step 5: Create a Dashboard

1. **Create a New Dashboard:**

   - Click on **Dashboards** > **+ New** > **Dashboard**.
   - Click **Add new panel**.

2. **Configure the Panel:**

   - Choose the metric you want to visualize, e.g., `node_cpu_seconds_total`.
   - Set the necessary visualization options.
   - Save and name your dashboard.

### Security Considerations

- **Authentication and Authorization:** Ensure you have proper user authentication and role-based access control enabled in Grafana.
- **Data Encryption:** Use HTTPS for Grafana and Prometheus. Configure TLS certificates for secure data transport.
- **Firewall Rules:** Only allow necessary ports to be accessible (e.g., 9090 for Prometheus, 3000 for Grafana) and restrict access to trusted IPs.

### Troubleshooting

- **Prometheus Not Starting:** Check if the configuration file (`prometheus.yml`) has any syntax errors using `promtool check config prometheus.yml`.
- **Node Exporter Metrics Not Visible:** Ensure Node Exporter is running and accessible at `localhost:9100`.
- **Grafana Unable to Connect to Prometheus:** Verify the Prometheus server is running and accessible from the Grafana server.

### Conclusion

By following this guide, you have set up a robust monitoring solution using Prometheus and Grafana. This setup allows you to collect metrics from your infrastructure and visualize them in real-time, helping you to maintain and optimize your systems effectively. Remember to regularly update your software to the latest versions to benefit from new features and security updates. Happy monitoring!