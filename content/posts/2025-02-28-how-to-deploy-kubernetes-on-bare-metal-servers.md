---
title: "How to deploy Kubernetes on bare-metal servers"
date: 2025-02-28
draft: false
toc: true
tags: ["Deploy", "Kubernetes", "On", "Bare", "Metal"]
categories: ["Automation", "Containerization"]
summary: "A comprehensive guide on How to deploy Kubernetes on bare-metal servers."
---

# How to deploy Kubernetes on bare-metal servers

Deploying Kubernetes on bare-metal servers can provide high performance, flexibility, and control over your infrastructure. Unlike cloud-based solutions, bare-metal deployments require careful planning and configuration. This tutorial will guide you through setting up Kubernetes on bare-metal servers, covering prerequisites, step-by-step deployment, security considerations, and troubleshooting tips.

## Prerequisites

Before you begin the deployment process, ensure you have the following prerequisites:

- **Bare-metal servers**: You'll need a minimum of three servers (one master and two nodes) to form a Kubernetes cluster.
- **Network configuration**: Ensure that all servers are connected to a reliable network with static IP addresses.
- **Linux OS**: All servers should run a supported version of Linux, such as Ubuntu 20.04 or CentOS 7/8.
- **SSH access**: Configure SSH access to all servers for remote management.
- **Sudo privileges**: Ensure you have sudo privileges on all servers.
- **Basic knowledge**: Familiarity with Linux command-line operations and basic networking concepts.

## Step-by-step Guide

### 1. Prepare the Environment

#### Update and Upgrade Packages

First, ensure that all your servers are up-to-date with the latest security patches and software updates.

```bash
sudo apt update && sudo apt upgrade -y
```

#### Disable Swap

Kubernetes requires swap to be disabled to function correctly.

```bash
sudo swapoff -a
sudo sed -i '/ swap / s/^/#/' /etc/fstab
```

#### Install Docker

Kubernetes uses container runtimes, such as Docker, to run containers. Install Docker on all servers:

```bash
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt update
sudo apt install -y docker-ce
```

Ensure Docker starts on boot:

```bash
sudo systemctl enable docker
```

### 2. Install Kubernetes Components

#### Add Kubernetes Repository

Add the Kubernetes apt repository to your sources list:

```bash
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee -a /etc/apt/sources.list.d/kubernetes.list
sudo apt update
```

#### Install kubeadm, kubelet, and kubectl

Install the necessary Kubernetes components on each server:

```bash
sudo apt install -y kubelet kubeadm kubectl
sudo apt-mark hold kubelet kubeadm kubectl
```

### 3. Initialize the Kubernetes Master Node

On the master node, initialize the Kubernetes cluster:

```bash
sudo kubeadm init --pod-network-cidr=192.168.0.0/16
```

After the command completes, you will see instructions to execute the `kubeadm join` command on the other nodes. Save this output for later use.

#### Configure kubectl

Set up the local kubeconfig for kubectl:

```bash
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

### 4. Set Up Pod Network

Install a pod network add-on to allow communication between pods. Here, we'll use Calico:

```bash
kubectl apply -f https://docs.projectcalico.org/manifests/calico.yaml
```

### 5. Join Worker Nodes to the Cluster

Run the `kubeadm join` command on each worker node. Replace `<kubeadm-join-command>` with the command saved from the master node initialization:

```bash
sudo kubeadm join <kubeadm-join-command>
```

### 6. Verify the Cluster

Back on the master node, verify that the nodes are successfully joined and ready:

```bash
kubectl get nodes
```

You should see a list of nodes with the status `Ready`.

## Security Considerations

- **Firewall settings**: Ensure that necessary ports are open for communication between Kubernetes components:
  - `6443` (Kubernetes API Server)
  - `2379-2380` (etcd server client API)
  - `10250` (Kubelet API)
  - `10251` (kube-scheduler)
  - `10252` (kube-controller-manager)
- **TLS certificates**: Use TLS for secure communications between components.
- **Role-Based Access Control (RBAC)**: Use RBAC to restrict access to cluster resources.
- **Network policies**: Implement network policies to control traffic flow between pods.

## Troubleshooting

- **Node not ready**: If a node shows as `NotReady`, check the kubelet logs for errors:
  ```bash
  sudo journalctl -u kubelet
  ```
- **Pod network issues**: If pods cannot communicate, ensure the network add-on is installed and configured correctly.
- **Resource constraints**: Monitor node resources (CPU, memory) to prevent overload.

## Conclusion

Deploying Kubernetes on bare-metal servers involves several steps but provides greater control and performance. By following this guide, you should have a functioning Kubernetes cluster ready to deploy containerized applications. Always monitor your cluster and apply best practices for security and resource management to ensure a stable and secure environment.