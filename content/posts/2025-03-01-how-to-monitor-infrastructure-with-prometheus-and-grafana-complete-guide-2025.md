---
title: "How to monitor infrastructure with Prometheus and Grafana - Complete Guide 2025"
date: 2025-03-01
draft: false
toc: true
tags: ["Monitor", "Infrastructure", "Prometheus", "Grafana", "Complete"]
categories: ["Infrastructure", "Automation"]
summary: "A comprehensive guide on How to monitor infrastructure with Prometheus and Grafana - Complete Guide 2025."
---

# How to monitor infrastructure with Prometheus and Grafana - Complete Guide 2025

Monitoring infrastructure is crucial for maintaining the health and performance of your systems. Prometheus and Grafana are popular open-source tools used for this purpose. This guide will walk you through setting up Prometheus and Grafana to monitor your infrastructure effectively.

## Introduction

Prometheus is a powerful time-series database designed for real-time monitoring and alerting. It collects metrics from configured targets at specified intervals, evaluates rule expressions, and can trigger alerts if certain conditions are met.

Grafana, on the other hand, is a visualization tool that helps you create interactive and dynamic dashboards. By integrating with Prometheus, it allows you to visualize and analyze the data collected by Prometheus.

In this guide, we'll cover the installation and configuration of Prometheus and Grafana, setting up monitoring for your infrastructure, and creating dashboards to visualize the collected data.

## Prerequisites

Before you begin, ensure you have the following:

1. **A Linux-based server**: This guide assumes you're using a server running a Linux distribution such as Ubuntu 20.04 or later.
2. **Basic knowledge of Linux command-line**: You'll need to execute commands and edit configuration files.
3. **Docker and Docker Compose (optional)**: If you prefer containerization, you can use Docker to run Prometheus and Grafana.
4. **Internet connectivity**: Both Prometheus and Grafana require downloading packages from the internet.

## Step-by-step Guide

### Step 1: Install Prometheus

1. **Download Prometheus**

   Start by downloading the latest version of Prometheus. Visit the [Prometheus download page](https://prometheus.io/download/) to find the latest release.

   ```bash
   cd /opt
   wget https://github.com/prometheus/prometheus/releases/download/v2.45.0/prometheus-2.45.0.linux-amd64.tar.gz
   tar xvfz prometheus-2.45.0.linux-amd64.tar.gz
   cd prometheus-2.45.0.linux-amd64
   ```

2. **Configure Prometheus**

   Create a basic configuration file named `prometheus.yml`.

   ```yaml
   global:
     scrape_interval: 15s

   scrape_configs:
     - job_name: 'prometheus'
       static_configs:
         - targets: ['localhost:9090']
   ```

3. **Start Prometheus**

   Run Prometheus using the following command:

   ```bash
   ./prometheus --config.file=prometheus.yml
   ```

   Prometheus should now be running on port 9090. You can verify by visiting `http://localhost:9090` in your web browser.

### Step 2: Install Grafana

1. **Download and Install Grafana**

   Download the latest Grafana package from the [Grafana website](https://grafana.com/grafana/download).

   ```bash
   wget https://dl.grafana.com/oss/release/grafana-enterprise_9.4.3_amd64.deb
   sudo dpkg -i grafana-enterprise_9.4.3_amd64.deb
   ```

2. **Start Grafana**

   Enable and start the Grafana service:

   ```bash
   sudo systemctl enable grafana-server
   sudo systemctl start grafana-server
   ```

   Grafana runs on port 3000 by default. Access it by visiting `http://localhost:3000` in your web browser.

3. **Configure Grafana**

   Log in with the default credentials (admin/admin) and set a new password when prompted.

### Step 3: Integrate Prometheus with Grafana

1. **Add Prometheus as a Data Source**

   - In Grafana, go to **Configuration > Data Sources**.
   - Click **Add data source** and select **Prometheus**.
   - Set the URL to `http://localhost:9090` and click **Save & Test** to verify the connection.

2. **Create a Dashboard**

   - Go to **Create > Dashboard** and click **Add new panel**.
   - In the panel editor, select **Prometheus** as the data source.
   - Enter a query, for example, `up`, to check if your targets are up.
   - Customize the visualization options and click **Apply** to save the panel.

### Step 4: Monitor Infrastructure Services

1. **Install Node Exporter (for Linux server metrics)**

   Node Exporter collects system metrics such as CPU and memory usage.

   ```bash
   cd /opt
   wget https://github.com/prometheus/node_exporter/releases/download/v1.6.0/node_exporter-1.6.0.linux-amd64.tar.gz
   tar xvfz node_exporter-1.6.0.linux-amd64.tar.gz
   cd node_exporter-1.6.0.linux-amd64
   ./node_exporter
   ```

2. **Update Prometheus Configuration**

   Add Node Exporter to the `prometheus.yml` configuration:

   ```yaml
   scrape_configs:
     - job_name: 'node_exporter'
       static_configs:
         - targets: ['localhost:9100']
   ```

3. **Reload Prometheus**

   Reload Prometheus to apply the new configuration. You can do this by sending a SIGHUP signal:

   ```bash
   kill -HUP $(pgrep prometheus)
   ```

4. **Visualize Node Metrics in Grafana**

   - Go to your Grafana dashboard and create a new panel.
   - Use queries like `node_cpu_seconds_total` or `node_memory_MemAvailable_bytes` to visualize system metrics.

## Security Considerations

1. **Network Security**

   - Ensure Prometheus and Grafana are not exposed to the public internet without proper security measures.
   - Use firewalls to restrict access to the services.

2. **Authentication and Authorization**

   - Configure authentication for Grafana, especially if accessible over the internet.
   - Use Grafana's built-in user management to control access to dashboards.

3. **Secure Data Transmission**

   - Enable HTTPS for both Prometheus and Grafana by configuring SSL/TLS certificates.

## Troubleshooting

1. **Prometheus Not Starting**

   - Check the logs for error messages using `./prometheus --config.file=prometheus.yml --log.level=debug`.
   - Verify configuration syntax and ensure there are no typos.

2. **Grafana Cannot Connect to Prometheus**

   - Ensure Prometheus is running and accessible at the specified URL.
   - Check network configurations and firewall rules.

3. **No Data in Grafana Dashboards**

   - Confirm that Prometheus is scraping metrics correctly by checking the targets page at `http://localhost:9090/targets`.
   - Verify that your queries in Grafana are correct and that the time range is appropriate.

## Conclusion

By following this guide, you should have a basic monitoring setup using Prometheus and Grafana. These tools provide powerful capabilities for collecting, querying, and visualizing metrics. As you gain familiarity, you can explore advanced features such as alerting, templating, and integration with other data sources.

Remember, monitoring is an ongoing process. Regularly review and update your dashboards and alerts to reflect the evolving needs of your infrastructure. With Prometheus and Grafana, you'll be well-equipped to maintain the health and performance of your systems.