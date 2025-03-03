---
ShowBreadCrumbs: true
ShowPostNavLinks: true
ShowReadingTime: true
ShowRssButtonInSectionTermList: true
ShowWordCount: true
TocOpen: false
UseHugoToc: true
author: Auto Blog Generator
comments: true
date: '2025-03-03'
description: A guide on Kubernetes cluster on Raspberry Pi
disableHLJS: false
disableShare: false
draft: false
hideSummary: false
hidemeta: false
searchHidden: false
showToc: true
tags:
- Kubernetes
- Raspberry Pi
- container orchestration
- IoT
- edge computing
title: "Setting Up a Kubernetes Cluster on Raspberry Pi: A Beginner\u2019s Guide"
---

In the age where cloud computing and container orchestration are revolutionizing the tech industry, understanding how to deploy and manage containerized applications is crucial. Kubernetes, an open-source platform designed to automate deploying, scaling, and operating application containers, stands out as a leader in this space. But what if you could learn and experiment with Kubernetes without the need for expensive cloud resources? Enter the Raspberry Pi, a low-cost, credit-card-sized computer that can serve as an excellent platform for learning Kubernetes. This guide will walk you through setting up a Kubernetes cluster on Raspberry Pi, providing a hands-on learning experience with this powerful tool.

## Why Kubernetes on Raspberry Pi Matters

The combination of Kubernetes and Raspberry Pi offers a unique opportunity for enthusiasts, students, and professionals to grasp the fundamentals of container orchestration in a tangible, cost-effective manner. It demystifies the complexities of Kubernetes by allowing you to build a mini-cluster at home. This hands-on approach accelerates learning, making it easier to transfer skills to larger, more complex environments.

## Prerequisites

- **Raspberry Pi 4** (at least 2GB model, but 4GB or 8GB recommended) x 3
- MicroSD cards (16GB or larger) x 3
- MicroSD card reader
- Power supply and cables
- An ethernet switch and cables (or a reliable WiFi setup)
- Latest version of Raspberry Pi OS Lite flashed on each MicroSD card
- Access to a router for network configuration

## Step 1: Initial Setup of Raspberry Pi

1. Flash Raspberry Pi OS Lite onto each MicroSD card using a tool like balenaEtcher.
2. Insert the MicroSD cards into your Raspberry Pis, connect them to your network, and power them on.
3. SSH into each Raspberry Pi using its IP address (discoverable from your router or a network scanning tool like Angry IP Scanner).

   ```
   ssh pi@raspberrypi.local
   ```

4. Change the default password for security reasons.

## Step 2: Network Configuration

It's crucial to assign static IP addresses to your Raspberry Pis to ensure that the nodes can communicate with each other reliably.

1. Edit the `dhcpcd.conf` file on each Raspberry Pi:

   ```
   sudo nano /etc/dhcpcd.conf
   ```

2. Add the following lines at the end, substituting `eth0` with `wlan0` if using WiFi, and adjusting the IP address as needed:

   ```
   interface eth0
   static ip_address=192.168.1.[20-22]/24
   static routers=192.168.1.1
   static domain_name_servers=8.8.8.8
   ```

3. Reboot each Raspberry Pi to apply the changes.

## Step 3: Install Kubernetes

We'll use k3s, a lightweight Kubernetes distribution designed for edge computing, IoT, and similar environments, which is perfect for Raspberry Pi.

1. On one Raspberry Pi (the master node), install k3s:

   ```
   curl -sfL https://get.k3s.io | sh -
   ```

2. Once the installation completes, retrieve the node token required to join worker nodes to the cluster:

   ```
   sudo cat /var/lib/rancher/k3s/server/node-token
   ```

3. On the other Raspberry Pis (worker nodes), join them to the cluster using the IP address of your master node and the node token:

   ```
   curl -sfL https://get.k3s.io | K3S_URL=https://<master_node_ip>:6443 K3S_TOKEN=<node_token> sh -
   ```

## Step 4: Verifying the Cluster

1. On the master node, check the status of the cluster:

   ```
   kubectl get nodes
   ```

You should see all your nodes listed, indicating that your cluster is up and running.

## Step 5: Deploying Your First Application

Let's deploy a simple Nginx application to test the cluster.

1. Create a deployment on the cluster:

   ```
   kubectl create deployment nginx --image=nginx
   ```

2. Expose the deployment:

   ```
   kubectl expose deployment nginx --port=80 --type=NodePort
   ```

3. Find the port assigned to your Nginx service:

   ```
   kubectl get services
   ```

4. Access the Nginx application by navigating to `<any_node_ip>:<NodePort>` in your web browser.

## Conclusion

Congratulations! You've just set up a Kubernetes cluster on Raspberry Pi, making a significant step towards mastering container orchestration. This project not only provides a comprehensive understanding of Kubernetes' workings but also empowers you to experiment with containerized applications in a real-world environment. Whether you're a student, hobbyist, or professional, the skills acquired from this setup are invaluable and transferable to larger scale deployments.

Remember, this is just the beginning. Explore further by deploying more complex applications, experimenting with persistent storage, or even integrating CI/CD pipelines into your cluster. The possibilities are endless, and your journey into Kubernetes has just begun.

**Key Takeaways:**

- Kubernetes can run on low-cost hardware like Raspberry Pi, making it accessible for learning and experimentation.
- Setting up a Kubernetes cluster involves configuring the network, installing Kubernetes, and joining nodes to the cluster.
- Deploying applications on your cluster allows you to gain hands-on experience with Kubernetes functionalities.

Happy exploring!

---