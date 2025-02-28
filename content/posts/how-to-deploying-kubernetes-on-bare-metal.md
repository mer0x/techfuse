---
title: "How to deploying Kubernetes on bare-metal"
date: "2025-02-28T16:11:13Z"
tags: ["Self-Hosting", "DevOps", "Homelab", "Networking"]
categories: ["IT Tutorials"]
draft: false
---
# How to Deploy Kubernetes on Bare-Metal: A Detailed Technical Tutorial

## Introduction

Kubernetes has become a cornerstone for managing containerized applications in production environments. Although cloud platforms like AWS, Google Cloud, and Azure provide powerful managed Kubernetes services, a growing number of organizations are opting to deploy Kubernetes on bare-metal servers. This approach offers increased control, improved performance, and potentially lower costs due to minimized dependencies on cloud vendors. In this comprehensive guide, we will walk through the steps to successfully deploy Kubernetes on bare-metal servers.

### Why Choose Bare-Metal for Kubernetes?

- **Performance**: Bare-metal deployments can yield better performance due to direct hardware access and no virtualization overhead.
- **Control**: Organizations maintain full control over the software and hardware stack.
- **Cost-Effectiveness**: Cost savings can be substantial in scenarios with high resource requirements.
- **Security**: Dedicated hardware can reduce the attack surface compared to multitenant cloud environments.

### Tools for Bare-Metal Kubernetes

In this tutorial, we will utilize the following tools:

- **Docker**: For container management.
- **Ansible**: For automating deployment and configuration.
- **Proxmox**: As a hypervisor to manage virtual machines if needed.
- **Cloudflare**: To manage domain and SSL certificates.

Let’s get started.

## Prerequisites

Before we delve into deploying Kubernetes on bare-metal, ensure you have the following prerequisites covered:

- Access to a set of bare-metal servers (at least three for a HA setup).
- Ubuntu 20.04 LTS installed on these servers.
- Basic knowledge of Linux command line.
- Administrative access to your DNS records (Cloudflare account).
- Ansible installed on a control node.

```bash
# Install Ansible on your control node
sudo apt update && sudo apt install -y ansible
```

Ensure your servers are networked together and you have SSH access from your control node.

## Implementation

### 1. Set up Docker on Each Node

You'll need Docker installed as Kubernetes will use it as its container runtime.

```bash
# Enable Docker repository and install Docker
sudo apt update
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt update
sudo apt install -y docker-ce
```

### 2. Configure Ansible Inventory

Create an Ansible inventory file with the list of your servers:

```ini
# inventory.ini
[kubemaster]
master1 ansible_host=192.168.1.10

[kubenodes]
node1 ansible_host=192.168.1.11
node2 ansible_host=192.168.1.12

[all:vars]
ansible_python_interpreter=/usr/bin/python3
```

### 3. Prepare Ansible Playbook

Create an Ansible playbook to install Kubernetes essentials.

```yaml
# kubernetes.yml
- hosts: all
  become: yes
  tasks:
    - name: Install dependencies
      apt:
        name: "{{ item }}"
        state: present
      loop:
        - apt-transport-https
        - curl

    - name: Add Kubernetes apt-key
      apt_key:
        url: https://packages.cloud.google.com/apt/doc/apt-key.gpg
        state: present

    - name: Add Kubernetes repository
      apt_repository:
        repo: "deb http://apt.kubernetes.io/ kubernetes-xenial main"

    - name: Install Kubernetes components
      apt:
        name: "{{ item }}"
        state: present
      loop:
        - kubelet
        - kubeadm
        - kubectl

    - name: Prevent automatic updates
      apt_mark:
        name: "{{ item }}"
        state: hold
      loop:
        - kubelet
        - kubeadm
        - kubectl
```

### 4. Execute the Ansible Playbook

Run your Ansible playbook to configure the bare-metal servers.

```bash
ansible-playbook -i inventory.ini kubernetes.yml
```

### 5. Initialize Kubernetes on the Master Node

SSH into your master node to initialize the Kubernetes cluster:

```bash
sudo kubeadm init --pod-network-cidr=192.168.0.0/16
```

Follow post-init instructions provided by `kubeadm` to configure `kubectl` access.

### 6. Configure Pod Network

Apply a networking solution compatible with Kubernetes:

```bash
kubectl apply -f https://docs.projectcalico.org/v3.14/manifests/calico.yaml
```

### 7. Join Worker Nodes

SSH into each worker node and join them to the cluster using the token generated during master initialization:

```bash
kubeadm join <master-ip>:6443 --token <token> --discovery-token-ca-cert-hash sha256:<hash>
```

### 8. Set Up DNS and SSL using Cloudflare

Configure your domain in Cloudflare to point to your Kubernetes master ingress IP. Use Cloudflare SSL/TLS settings to manage certificates.

## Troubleshooting

### Common Issues:

- **Node Not Ready**: Check `kubectl get nodes` for conditions such as "NotReady". Ensure all services are running and network settings are correct.
- **Token Expiry for Worker Nodes**: Update the token using `kubeadm token create` and retry joining nodes.
- **DNS Resolution Issues**: Ensure CoreDNS pods are running and configured correctly.

Run `kubectl describe pod <pod-name>` for more detailed diagnostics.

### Protips:

- **Monitoring and Logging**: Integrate Prometheus and Grafana for monitoring. Use ELK Stack for logging.
- **Backup Configuration**: Regularly back up your configurations and consider tools like Velero for disaster recovery.

## Conclusion

Deploying Kubernetes on bare-metal is a rewarding endeavor that provides enhanced performance, security, and cost control. While it requires more upfront effort compared to cloud-managed services, the gains can be significant for workloads demanding robust and tailored infrastructure setups.

By following this guide, you now have the knowledge to set up and run a Kubernetes cluster on your own hardware. As you gain experience, consider diving deeper into Kubernetes native tools like Helm for packaging applications and exploring service mesh technologies such as Istio for advanced traffic management.

Embrace the power of the cloud on your own terms and make the most of Kubernetes' capabilities on bare-metal infrastructure.