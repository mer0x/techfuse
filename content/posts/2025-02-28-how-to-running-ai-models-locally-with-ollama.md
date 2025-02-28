---
title: "How to running AI models locally with Ollama"
date: 2025-02-28
tags: ["Self-Hosting", "DevOps", "Homelab", "Networking"]
categories: ["IT Tutorials"]
draft: false
---
# How to Run AI Models Locally with Ollama

## Introduction

In the rapidly advancing world of artificial intelligence, running AI models locally is an emerging trend, giving enthusiasts and developers the power to harness AI without relying solely on cloud services. This approach provides greater control over data, security, and customization. Ollama is a robust tool designed for running AI models locally. By enabling AI model deployment within a self-controlled environment, Ollama caters to organizations and individuals seeking to integrate AI capabilities securely and efficiently.

Self-hosting AI models with Ollama has numerous advantages, including increased privacy, reduced latency, lower costs, and the ability to run AI workloads offline. This tutorial will guide you through the process of running AI models locally with Ollama while leveraging Docker, Ansible, Proxmox, and Cloudflare. By the end of this tutorial, you'll be equipped with the knowledge to effectively deploy and manage AI models in-house.

## Prerequisites

Before you begin, ensure you have the following prerequisites:

1. **Basic Understanding of AI and Machine Learning:** Familiarity with AI model deployment processes will be beneficial.
2. **Linux-Based System:** Knowledge of Linux terminal commands and system configuration.
3. **Docker Installed:** Docker streamlines application deployment and management by providing containerization capabilities.
4. **Ansible Installed:** Automate provisioning and configuration management tasks with Ansible.
5. **Proxmox VE Installed (Optional):** Virtualize environments to manage your AI workloads effectively.
6. **Cloudflare Account (Optional):** Deploy secure web services for your AI model using Cloudflare.
7. **Ollama Account and Access to Model Data:** Ensure that you have Ollama configured with the necessary models ready to be deployed locally.

## Step-by-Step Implementation

### Step 1: Set Up Your Environment

#### 1.1 Install Docker

Docker is crucial for creating containerized environments to run AI models. Follow the instructions for your operating system from Docker's official documentation:

```bash
# For Ubuntu
sudo apt-get update
sudo apt-get install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker
```

#### 1.2 Install Ansible

Ansible will help automate the deployment process:

```bash
# For Ubuntu
sudo apt-get update
sudo apt-get install -y ansible
```

### Step 2: Configure Ollama

#### 2.1 Download and Install Ollama

Access [Ollama's official website](https://ollama.com) and download the latest version appropriate for your system. Follow the installation instructions provided by Ollama.

#### 2.2 Prepare the AI Model

Ensure you have access to the AI model data files that you wish to run locally. Ollama supports a variety of AI models, so ensure compatibility.

### Step 3: Deploy AI Model with Docker and Ollama

#### 3.1 Create Dockerfile

Create a Dockerfile in the root directory to define your AI model environment:

```dockerfile
# Step 1: Use a base image
FROM ubuntu:20.04

# Step 2: Install dependencies and copy AI model data
RUN apt-get update && apt-get install -y \
  python3 \
  python3-pip

WORKDIR /app

COPY . /app

# Step 3: Install Ollama
RUN pip3 install ollama

# Step 4: Expose necessary ports and define default command
EXPOSE 5000
CMD ["ollama", "serve"]
```

#### 3.2 Build and Run the Docker Container

```bash
docker build -t ollama-local-ai .
docker run -d -p 5000:5000 ollama-local-ai
```

### Step 4: Automate Deployment with Ansible

#### 4.1 Create Ansible Playbook

Define an Ansible playbook to automate deployment steps:

```yaml
---
- name: Deploy AI Model Locally with Ollama
  hosts: localhost
  tasks:
    - name: Pull Docker Image
      docker_image:
        name: ollama-local-ai
        source: build
        path: /path/to/dockerfile

    - name: Run Docker Container
      docker_container:
        name: ollama-ai-service
        image: ollama-local-ai
        state: started
        ports:
          - "5000:5000"
```

#### 4.2 Run the Ansible Playbook

```bash
ansible-playbook deploy-ollama-ai.yml
```

### Step 5: Optimize Network Security with Cloudflare (Optional)

#### 5.1 Configure Cloudflare

- Set up a Cloudflare account and ensure your domain is linked.
- Enable SSL/TLS encryption to secure communications.

#### 5.2 Set Up SSL/TLS

Navigate to the SSL/TLS section and enable "Full" mode for HTTPS traffic.

### Step 6: Use Proxmox for Virtualization (Optional)

Virtualize your AI model to manage workloads effectively, utilizing Proxmox:

- Install Proxmox VE following [Proxmox's official documentation](https://www.proxmox.com/en/proxmox-ve).
- Create and configure virtual machines to host your AI applications, optimizing resources.

## Troubleshooting

### Common Issues

- **Docker Build Fails:** Ensure all dependencies are correctly installed in the Dockerfile.
- **Ansible Errors:** Check Ansible's syntax and YAML formatting. Ensure inventory files are configured correctly.
- **Network Latency:** Optimize Docker and network configurations. Use Cloudflare's CDN for efficient traffic routing.

## Conclusion

Running AI models locally with Ollama opens the door to numerous possibilities, from increased data security to better cost efficiency. This tutorial outlined the essential steps to deploy AI models in a self-hosted environment using Docker, Ansible, and optional tools like Proxmox and Cloudflare. By empowering developers and organizations with local AI capabilities, you can drive innovation, optimize operations, and maintain a competitive edge in the ever-evolving AI landscape. Now, with this knowledge, you can confidently embark on your AI journey with Ollama.