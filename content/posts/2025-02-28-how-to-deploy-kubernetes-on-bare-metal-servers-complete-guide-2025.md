---
title: "How to deploy Kubernetes on bare-metal servers - Complete Guide 2025"
date: 2025-02-28
draft: false
toc: true
tags: ["Deploy", "Kubernetes", "On", "Bare", "Metal"]
categories: ["Automation", "Containerization"]
summary: "A comprehensive guide on How to deploy Kubernetes on bare-metal servers - Complete Guide 2025."
---

# How to deploy Kubernetes on bare-metal servers - Complete Guide 2025

Deploying Kubernetes on bare-metal servers can be a rewarding endeavor, providing you with maximum control over your infrastructure. In this comprehensive guide, we walk you through the entire process, from setting up your environment to securing your cluster. By the end of this guide, you will have a robust Kubernetes setup running on your physical machines.

## Introduction

Kubernetes is an open-source container orchestration platform that automates many of the manual processes involved in deploying, managing, and scaling containerized applications. While cloud providers offer managed Kubernetes services, deploying on bare-metal gives you more freedom and control over your hardware resources, network configurations, and security policies.

Deploying Kubernetes on bare-metal requires careful planning and execution, but it can lead to superior performance and cost-effectiveness. This guide will take you through the setup process, step-by-step, ensuring you have a working Kubernetes cluster tailored to your needs.

## Prerequisites

Before we dive into the deployment process, let's make sure we have everything we need:

- **Hardware Requirements**: At least 3 servers (1 master node and 2 worker nodes) with the following minimum specifications:
  - CPU: 2 cores
  - RAM: 4 GB
  - Storage: 20 GB SSD
  - Network: 1 Gbps NIC

- **Operating System**: Ubuntu 22.04 LTS is recommended for its stability and support.

- **Networking**: Ensure that all servers have static IP addresses and can communicate with each other.

- **Access**: SSH access to all servers with root privileges.

- **Tools**: Install `kubectl` on your local machine for cluster management.

## Step-by-step Guide

### Step 1: Prepare the Servers

1. **Set Hostnames and Update Packages**:
   ```bash
   sudo hostnamectl set-hostname <hostname>
   sudo apt update && sudo apt upgrade -y
   ```

2. **Modify `/etc/hosts`**:
   Add entries for each node to resolve hostnames to IP addresses.
   ```bash
   192.168.1.10 master-node
   192.168.1.11 worker-node1
   192.168.1.12 worker-node2
   ```

3. **Disable Swap**:
   Kubernetes requires swap to be disabled for proper scheduling.
   ```bash
   sudo swapoff -a
   sudo sed -i '/ swap / s/^\(.*\)$/#\1/g' /etc/fstab
   ```

4. **Load Kernel Modules**:
   ```bash
   cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
   overlay
   br_netfilter
   EOF

   sudo modprobe overlay
   sudo modprobe br_netfilter
   ```

5. **Configure sysctl**:
   ```bash
   cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
   net.bridge.bridge-nf-call-ip6tables = 1
   net.bridge.bridge-nf-call-iptables = 1
   net.ipv4.ip_forward = 1
   EOF

   sudo sysctl --system
   ```

### Step 2: Install Docker

Docker is the container runtime we will use for Kubernetes.

1. **Install Docker**:
   ```bash
   sudo apt-get install -y ca-certificates curl gnupg
   sudo mkdir -p /etc/apt/keyrings
   curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

   echo \
   "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

   sudo apt-get update
   sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
   ```

2. **Enable and Start Docker**:
   ```bash
   sudo systemctl enable docker
   sudo systemctl start docker
   ```

### Step 3: Install Kubernetes Components

1. **Add Kubernetes APT Repository**:
   ```bash
   sudo apt-get update
   sudo apt-get install -y apt-transport-https ca-certificates curl
   sudo curl -fsSLo /etc/apt/trusted.gpg.d/kubernetes-archive-keyring.gpg \
       https://packages.cloud.google.com/apt/doc/apt-key.gpg

   echo "deb [signed-by=/etc/apt/trusted.gpg.d/kubernetes-archive-keyring.gpg] https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list
   ```

2. **Install kubeadm, kubelet, and kubectl**:
   ```bash
   sudo apt-get update
   sudo apt-get install -y kubelet kubeadm kubectl
   sudo apt-mark hold kubelet kubeadm kubectl
   ```

3. **Enable and start kubelet**:
   ```bash
   sudo systemctl enable kubelet
   sudo systemctl start kubelet
   ```

### Step 4: Initialize the Kubernetes Master Node

1. **Initialize the Cluster**:
   ```bash
   sudo kubeadm init --pod-network-cidr=192.168.0.0/16
   ```

2. **Configure kubectl for the root user**:
   ```bash
   mkdir -p $HOME/.kube
   sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
   sudo chown $(id -u):$(id -g) $HOME/.kube/config
   ```

3. **Deploy a Pod Network**:
   Use Calico as the network plugin.
   ```bash
   kubectl apply -f https://docs.projectcalico.org/manifests/calico.yaml
   ```

### Step 5: Join Worker Nodes to the Cluster

1. **Generate the Join Command**:
   On the master node, get the join command.
   ```bash
   kubeadm token create --print-join-command
   ```

2. **Execute the Join Command on Each Worker Node**:
   Run the command generated in the previous step on each worker node.

### Step 6: Verify the Cluster

1. **Check Node Status**:
   ```bash
   kubectl get nodes
   ```

2. **Check Pod Status**:
   ```bash
   kubectl get pods --all-namespaces
   ```

## Security Considerations

- **Network Policies**: Implement network policies to control traffic between pods and external networks.

- **RBAC**: Use Role-Based Access Control (RBAC) to restrict permissions and access to Kubernetes resources.

- **TLS Encryption**: Ensure all communications within the cluster are encrypted with TLS.

- **Regular Updates**: Keep Kubernetes components and plugins updated to protect against vulnerabilities.

## Troubleshooting

- **Node Not Ready**: If a node is not in the "Ready" state, check the kubelet service and network configuration.

- **Pods Not Starting**: Check pod logs for errors and ensure the network plugin is properly configured.

- **Network Issues**: Verify that all nodes can communicate over the network by pinging each other.

## Conclusion

Deploying Kubernetes on bare-metal servers provides you with a powerful platform for managing containerized applications with full control over your hardware. By following this guide, you should have a fully functional Kubernetes cluster ready for production workloads. Remember to continuously monitor your cluster and apply security best practices to maintain a secure and efficient environment.

This guide serves as a foundation, and as you grow more familiar with Kubernetes, you can explore advanced topics such as persistent storage, multi-cluster management, and hybrid cloud solutions. Happy clustering!