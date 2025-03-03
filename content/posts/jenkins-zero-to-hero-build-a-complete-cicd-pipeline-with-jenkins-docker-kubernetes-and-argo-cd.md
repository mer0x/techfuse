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
description: 'A guide on Exploring Jenkins-Zero-To-Hero: Install Jenkins, configure
  Docker as slave, set up cicd, deploy applications to k8s using Argo CD in GitOps
  way.'
disableHLJS: false
disableShare: false
draft: false
hideSummary: false
hidemeta: false
searchHidden: false
showToc: true
tags:
- Jenkins
- Docker
- Kubernetes
- Argo CD
- GitOps
title: 'Jenkins Zero-to-Hero: Build a Complete CI/CD Pipeline with Jenkins, Docker,
  Kubernetes, and Argo CD'
---

Continuous Integration and Continuous Delivery (CI/CD) practices empower teams to release software faster, safer, and more reliably. Jenkins, Docker, Kubernetes (k8s), and Argo CD form a powerful stack that can greatly streamline your development workflow. This guide will walk you through installing Jenkins, configuring Docker as a Jenkins agent, setting up a CI/CD pipeline, and deploying applications to Kubernetes using Argo CD in a GitOps manner.

By the end of this tutorial, you'll have a fully automated CI/CD workflow designed for modern, cloud-native applications.

---

## Prerequisites

Before starting, make sure you have the following installed and configured:

- Basic understanding of Docker and Kubernetes
- Kubernetes cluster (e.g., Minikube, Docker Desktop Kubernetes, or cloud-managed clusters like AWS EKS, Google GKE, Azure AKS)
- Installed `kubectl` command-line tool
- Docker installed and configured
- GitHub or GitLab repository for version control management

---

## Step 1: Installing Jenkins on Kubernetes

To run Jenkins effectively in your Kubernetes cluster, we'll deploy it using Helm.

### Install Helm (if not already installed)

```bash
curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash
```

### Add Jenkins Helm repo and install Jenkins

```bash
helm repo add jenkins https://charts.jenkins.io
helm repo update
kubectl create namespace jenkins
helm install jenkins jenkins/jenkins --namespace jenkins
```

### Retrieve Jenkins initial admin password

Wait a few minutes for Jenkins to start, then retrieve the admin password:

```bash
kubectl exec --namespace jenkins -it svc/jenkins -c jenkins -- cat /var/jenkins_home/secrets/initialAdminPassword
```

Copy this password, then open the Jenkins web interface using port forwarding:

```bash
kubectl --namespace jenkins port-forward svc/jenkins 8080:8080
```

Navigate to `http://localhost:8080`, paste the retrieved password, and follow the setup wizard. Install recommended plugins or choose custom plugins according to your needs.

---

## Step 2: Configure Docker as Jenkins Agent (Slave)

Using Docker containers as Jenkins agents provides flexibility and scalability.

### Install Docker plugin in Jenkins

Navigate to Jenkins Dashboard → Manage Jenkins → Manage Plugins. Search for "Docker Pipeline" and "Docker Commons" plugins, then install them.

### Configure Docker Cloud in Jenkins

- Navigate to "Manage Jenkins" → "Manage Nodes and Clouds" → "Configure Clouds".
- Click "Add new cloud" and select "Docker".
- Configure Docker Host URI (usually `tcp://docker-host-ip:2375`) and test connection.

> **Note**: Make sure your Docker daemon allows TCP connection. For local testing, you can start Docker with TCP enabled:
```bash
dockerd -H tcp://0.0.0.0:2375 -H unix:///var/run/docker.sock
```

### Define Docker Agent in Jenkinsfile (Pipeline script example)

Here's a simple Jenkins pipeline script utilizing Docker agent:

```groovy
pipeline {
    agent {
        docker {
            image 'node:18-alpine' // Example image
            args '-u root:root'    // Run container as root (optional)
        }
    }
    stages {
        stage('Build') {
            steps {
                sh 'npm install'
                sh 'npm run build'
            }
        }
        stage('Test') {
            steps {
                sh 'npm test'
            }
        }
    }
}
```

---

## Step 3: Setting Up CI/CD Pipeline in Jenkins

Next, we'll set up a Jenkins pipeline job that integrates seamlessly with your Git repository.

### Create a new pipeline job

- From Jenkins dashboard, select "New Item".
- Enter a name, select "Pipeline", and click "OK".
- Configure your pipeline to pull Jenkinsfile from your Git repository.

Example Jenkinsfile (Declarative pipeline):

```groovy
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/yourusername/yourapp.git'
            }
        }
        stage('Build') {
            steps {
                sh './build.sh'
            }
        }
        stage('Docker Build and Push') {
            steps {
                script {
                    docker.build('yourdockerhubusername/yourapp:latest').push()
                }
            }
        }
    }
}
```

Make sure to configure Docker credentials in Jenkins to push images to Docker Hub or other registries.

---

## Step 4: Deploying Applications to Kubernetes using Argo CD (GitOps)

Argo CD allows declarative application deployment using Git as a single source of truth.

### Install Argo CD on Kubernetes

```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

### Access Argo CD UI

Port-forward Argo CD server:

```bash
kubectl port-forward svc/argocd-server -n argocd 8081:443
```

Open `https://localhost:8081` and log in with default credentials:

- Username: `admin`
- Password: Retrieve via CLI:

```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

### Create GitOps Repo for your Kubernetes Manifests

Create a new Git repository (e.g., `yourapp-k8s`) containing application deployment manifests:

Example Kubernetes deployment (`deployment.yaml`):

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: yourapp
spec:
  replicas: 2
  selector:
    matchLabels:
      app: yourapp
  template:
    metadata:
      labels:
        app: yourapp
    spec:
      containers:
      - name: yourapp
        image: yourdockerhubusername/yourapp:latest
        ports:
        - containerPort: 8080
```

### Configure Argo CD Application

In Argo CD UI, create a new application:

- Application name: `yourapp`
- Project: `default`
- Git Repository URL: URL to your GitOps repository (`yourapp-k8s`)
- Path: Path to manifests (e.g., `/`)
- Destination: Your Kubernetes cluster and namespace

Once saved, Argo CD automatically syncs your application with your Git repo. Any changes pushed to the Git repo automatically trigger deployment updates (true GitOps workflow).

---

## Conclusion

In this comprehensive guide, we covered how to:

- Install Jenkins using Helm on Kubernetes.
- Configure Docker as a Jenkins agent for isolated, scalable builds.
- Set up a CI/CD pipeline in Jenkins to build and test code.
- Deploy applications to Kubernetes using Argo CD in a GitOps approach.

By following GitOps practices, your deployments become reproducible, auditable, and easily manageable, significantly enhancing your development and operational efficiency.

---

**