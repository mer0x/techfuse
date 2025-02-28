---
date: 2025-02-28

# How to Run AI Models Locally with Ollama

## Introduction

In the rapidly advancing field of artificial intelligence, the ability to run models locally has monumental significance. Self-hosting AI models offers a level of control, security, and customization that cloud resources can't always guarantee. As data privacy and compliance regulations tighten, having your models running on-premises can ensure that sensitive data remains within your control.

Ollama emerges as a powerful option for those seeking to run AI models locally. By adopting a self-hosting approach, organizations can tailor solutions to meet specific needs without being tethered to cloud subscription models. This tutorial will guide you through the process of setting up AI models on local infrastructure using Ollama, utilizing modern tools like Docker, Ansible, and Proxmox to streamline the deployment process.

## Prerequisites

Before diving into the tutorial, ensure you have the following prerequisites:

1. **Technical Background**: Familiarity with Docker, Linux command-line interface, and basic networking.
2. **System Requirements**: A machine running Linux (Ubuntu 20.04+), with at least 16 GB RAM and a compatible GPU for optimal performance.
3. **Software**: 
   - Docker
   - Ansible
   - Proxmox (optional, for virtualization)
   - Ollama (download from their [official website](https://ollama.com))
4. **Network**: Ensure your local network is configured correctly, with access to the internet for downloading necessary packages and updates.

## Step-by-Step Implementation

### Step 1: Set Up the Environment

#### Installing Docker

Docker is an essential tool for containerizing applications and will serve as our primary platform for deploying AI models. Follow these steps to install Docker:

```bash
# Update your package index
sudo apt-get update

# Install prerequisite packages
sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common

# Add Docker's official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

# Add Docker stable repository
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

# Update the package index again
sudo apt-get update

# Install Docker CE
sudo apt-get install -y docker-ce

# Verify Docker installation
docker --version
```

#### Installing Proxmox (Optional)

Proxmox is a powerful open-source server virtualization management platform. Use it if you prefer setting up VMs rather than working directly on physical hardware:

1. Download the Proxmox VE ISO from [here](https://www.proxmox.com/en/downloads).
2. Create a bootable USB stick with the ISO.
3. Boot your machine from the USB stick and follow the installation prompts.

### Step 2: Deploy AI Model with Ollama

Download and set up Ollama locally on your machine:

1. Navigate to the Ollama downloads page and download the latest binary compatible with your operating system.

2. Make the binary executable:

    ```bash
    chmod +x ollama
    ```

3. Move the Ollama binary to your `/usr/local/bin` to make it globally accessible:

    ```bash
    sudo mv ollama /usr/local/bin/
    ```

4. Verify the installation:

    ```bash
    ollama --version
    ```

5. Prepare your Dockerfile for the AI model container:

    ```dockerfile
    FROM ubuntu:20.04

    # Install required packages
    RUN apt-get update && apt-get install -y \
        python3 \
        python3-pip \
        wget \
        build-essential

    # Install Ollama
    RUN wget <Download_Link_For_Ollama> -O ollama \
        && chmod +x ollama \
        && mv ollama /usr/local/bin/

    # Install necessary Python packages
    RUN pip3 install torch torchvision

    # Add your AI model code here
    COPY . /app
    WORKDIR /app
    ```

6. Build the Docker image:

    ```bash
    docker build -t ai-model .
    ```

7. Run the Docker container:

    ```bash
    docker run -d -p 5000:5000 ai-model
    ```

### Step 3: Automate Deployment with Ansible

Ansible simplifies repeat deployments. Create an Ansible playbook for Ollama deployment:

```yaml
---
- name: Deploy AI Model with Ollama
  hosts: all
  become: yes
  tasks:
  
  - name: Install Docker
    apt:
      name: docker-ce
      state: present

  - name: Copy AI Model container config
    copy:
      src: Dockerfile
      dest: /opt/ai-model/Dockerfile
      
  - name: Build and run AI Model container
    shell: |
      cd /opt/ai-model
      docker build -t ai-model .
      docker run -d -p 5000:5000 ai-model
```

Run the playbook using:

```bash
ansible-playbook -i inventory.yaml deploy_ollama_model.yaml
```

### Step 4: Optional Setup with Cloudflare

For accessibility, secure your local instance with Cloudflare. Sign up for an account, add your domain, and configure DNS settings to point to your local server's IP address. Utilize Cloudflare's tunneling feature for secure access.

## Troubleshooting

1. **Docker Container Fails to Start**: Check logs with `docker logs <container_id>` for error messages.
2. **Ollama Command Not Found**: Ensure the binary is in your path and installed correctly.
3. **Network Errors**: Confirm that firewalls or security groups allow traffic on the ports your application uses.

## Conclusion

Running AI models locally with Ollama offers significant flexibility and control, especially in data-sensitive environments. While it requires an upfront setup effort, the benefits of having scalable, secure, and customizable AI infrastructure are worthwhile. With tools like Docker, Ansible, and Proxmox, the process is streamlined, making it accessible even to those new to DevOps. Embrace the power of Ollama to supercharge your AI capabilities, on premises.

Remember to keep your environment updated regularly and experiment with new tools and configurations to optimize performance and security. Happy self-hosting!