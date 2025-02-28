---
title: "How to monitor infrastructure with Prometheus and Grafana"
date: 2025-02-28
draft: false
toc: true
tags: ["Monitor", "Infrastructure", "Prometheus", "Grafana"]
categories: ["Infrastructure", "Automation"]
summary: "A comprehensive guide on How to monitor infrastructure with Prometheus and Grafana."
---

# How to monitor infrastructure with Prometheus and Grafana

Monitoring infrastructure is crucial for ensuring the reliability and performance of your systems. Prometheus and Grafana are popular open-source tools that provide powerful capabilities for monitoring and visualization. This tutorial will guide you through the process of setting up Prometheus and Grafana to monitor infrastructure effectively.

## Introduction

Prometheus is a robust and scalable time-series database designed for real-time monitoring and alerting. It collects metrics from configured targets at given intervals, evaluates rule expressions, displays the results, and triggers alerts if certain conditions are observed.

Grafana, on the other hand, is a visualization tool that works seamlessly with Prometheus to provide users with real-time insights into their data. It allows the creation of custom dashboards to visualize metrics pulled from Prometheus.

In this tutorial, we will cover how to set up a basic monitoring system using Prometheus and Grafana, including the steps to configure them to collect and display metrics from a sample application.

## Prerequisites

Before proceeding, ensure that you have the following prerequisites:

- A Linux-based server or virtual machine with a recent version of Ubuntu or CentOS.
- Basic knowledge of Linux command-line operations.
- Docker installed on your system to facilitate easy deployment of Prometheus and Grafana.
- Access to a sample application or service that you wish to monitor. Alternatively, you can use a dummy application for testing purposes.

## Step-by-step Guide

### Step 1: Setting Up Prometheus

#### 1.1 Install Prometheus

First, let's deploy Prometheus using Docker. Execute the following commands to pull and run the Prometheus Docker image.

```bash
docker pull prom/prometheus

docker run -d --name=prometheus -p 9090:9090 \
  -v /path/to/prometheus.yml:/etc/prometheus/prometheus.yml \
  prom/prometheus
```

Ensure you replace `/path/to/prometheus.yml` with the actual path to your Prometheus configuration file.

#### 1.2 Configure Prometheus

Create a `prometheus.yml` configuration file. This file dictates the behavior of Prometheus, including which services to scrape for metrics.

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'example_service'
    static_configs:
      - targets: ['localhost:8080']
```

In this configuration, Prometheus will scrape metrics from a service running on `localhost` at port `8080` every 15 seconds.

### Step 2: Setting Up Grafana

#### 2.1 Install Grafana

Next, let's set up Grafana, also using Docker.

```bash
docker pull grafana/grafana

docker run -d --name=grafana -p 3000:3000 grafana/grafana
```

#### 2.2 Access Grafana

Open a web browser and navigate to `http://<server-ip>:3000`. You should see the Grafana login page. The default username and password are both `admin`. You will be prompted to change the password upon first login.

#### 2.3 Configure Grafana Data Source

Once logged in, set up Prometheus as a data source:

1. Click on the gear icon to access the Configuration menu.
2. Select "Data Sources".
3. Click "Add data source".
4. Choose "Prometheus" from the list.
5. Enter the Prometheus server URL, typically `http://<server-ip>:9090`.
6. Click "Save & Test" to verify the connection.

### Step 3: Building Dashboards

#### 3.1 Create a New Dashboard

1. Click on the "+" icon on the left sidebar and select "Dashboard".
2. Click "Add Query" to begin adding data visualizations.
3. Use the query editor to specify the metrics you wish to visualize. For instance, to display CPU usage, you might use a query like `rate(node_cpu_seconds_total[1m])`.

#### 3.2 Customize Panels

Grafana allows you to customize panels with different visualization options such as graphs, heatmaps, and tables. Adjust these settings to suit your monitoring needs.

### Step 4: Alerting

Prometheus and Grafana support alerting to notify you of potential issues.

#### 4.1 Configure Prometheus Alerts

Define alerting rules in `prometheus.yml`.

```yaml
rule_files:
  - "alerts.yml"
```

Create an `alerts.yml` file:

```yaml
groups:
- name: example_alerts
  rules:
  - alert: HighMemoryUsage
    expr: node_memory_Active_bytes > 1e+09
    for: 5m
    labels:
      severity: "warning"
    annotations:
      summary: "High memory usage detected"
```

#### 4.2 Configure Grafana Alerts

In Grafana, alerts can be set up directly on graphs:

1. Open a panel and click the "Alert" tab.
2. Define alert conditions and notification channels.
3. Save the panel.

### Security Considerations

Securing your monitoring setup is critical. Here are a few recommendations:

- **Authentication and Authorization:** Ensure Grafana is behind an authentication layer. Use OAuth, LDAP, or other authentication methods supported by Grafana.
- **Network Security:** Use firewalls to restrict access to Prometheus and Grafana ports. Consider setting up a VPN or using SSH tunnels for secure access.
- **TLS/SSL:** Configure TLS/SSL for Prometheus and Grafana to encrypt data in transit.
- **Access Controls:** Limit access to Prometheus and Grafana to only those who need it. Use Grafana's built-in user roles to manage permissions.

### Troubleshooting

#### Common Issues and Solutions

1. **Prometheus not scraping targets:**
   - Verify that the target service is running and accessible.
   - Check the scrape configuration in `prometheus.yml`.

2. **Grafana cannot connect to Prometheus:**
   - Ensure Prometheus is reachable at the specified URL.
   - Verify there are no network policies or firewalls blocking access.

3. **Database connection errors in Grafana:**
   - Check Grafana logs for detailed error messages.
   - Ensure the database settings in Grafana are correct.

### Conclusion

In this tutorial, we have set up a basic monitoring system using Prometheus and Grafana. We've covered how to install and configure both tools, create dashboards, and set up alerts. With these tools, you can gain valuable insights into your infrastructure and ensure the smooth operation of your services.

Continue to explore the extensive capabilities of Prometheus and Grafana to tailor them to your specific monitoring needs. Happy monitoring!