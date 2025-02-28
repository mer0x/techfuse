---
title: "Using GitHub Actions for CI/CD in self-hosted environments"
date: 2025-02-28
tags: ["Self-Hosting", "DevOps", "Homelab", "Networking"]
categories: ["IT Tutorials"]
draft: false
---


# Using GitHub Actions for CI/CD in Self-hosted Environments

GitHub Actions is a powerful platform that allows developers to automate tasks within their software development lifecycle. It seamlessly integrates with GitHub repositories, enabling continuous integration and deployment (CI/CD). While GitHub provides cloud-hosted runners, there are scenarios where you might want to use self-hosted runners, such as requiring specific hardware, software configurations, or enhanced control over the execution environment.

In this tutorial, we'll explore how to set up GitHub Actions for CI/CD in self-hosted environments, ensuring you leverage its full potential.

## Prerequisites

Before diving into implementation, ensure you have the following:

1. **GitHub Account**: A GitHub account to host your repositories and workflows.

2. **Repository**: A GitHub repository where you'll configure GitHub Actions.

3. **Self-hosted Runner**: A physical or virtual machine to act as a runner (could be on-premises or a cloud VM).

4. **Basic Knowledge of Git and CI/CD**: Familiarity with source control management and continuous integration/deployment concepts will be helpful.

5. **Permissions**: Admin access to the GitHub repository to add and manage self-hosted runners.

## Implementation

### Step 1: Setting Up a Self-hosted Runner

#### 1.1 Configuring the Runner

1. **Access Runner Settings**: Navigate to your GitHub repository, click on **Settings**, then **Actions**, and select **Runners**.

2. **Add Runner**: Click on **New self-hosted runner**. Choose the appropriate operating system (Linux, macOS, or Windows) for your environment.

3. **Download and Install**: Follow the instructions to download and install the runner application. This typically involves:
   - Downloading a compressed file (scripts, binaries), e.g., `actions-runner-linux-x64-2.285.1.tar.gz`.
   - Unpacking the archive and navigating to the directory where the runner will execute.

   ```shell
   $ tar xzf actions-runner-linux-x64-2.285.1.tar.gz
   ```

4. **Configure Runner**: Configure the runner with a unique token generated from GitHub. This involves executing a command such as:

   ```shell
   $ ./config.sh --url https://github.com/your-org/your-repo --token <RUNNER_TOKEN>
   ```

5. **Run the Runner**: Start the runner, which will register it with your GitHub repository.

   ```shell
   $ ./run.sh
   ```

#### 1.2 Verify Registration

Check for the self-hosted runner under the **Runners** section in the **GitHub Actions** tab. It should indicate an "Online" status if registered correctly.

### Step 2: Creating a Workflow

Create a GitHub Actions workflow file in your repository to use the self-hosted runner.

1. **Create a Workflow File**: In your code repository, navigate to `.github/workflows/`. Create a new YAML file, e.g., `ci-cd-pipeline.yml`.

2. **Define the Workflow**: Here's a simple example workflow for a Node.js application.

   ```yaml
   name: Node.js CI

   on:
     push:
       branches: [ main ]
     pull_request:
       branches: [ main ]

   jobs:
     build:
       runs-on: self-hosted

       steps:
       - uses: actions/checkout@v2

       - name: Set up Node.js
         uses: actions/setup-node@v2
         with:
           node-version: '14'

       - name: Install dependencies
         run: npm install

       - name: Run tests
         run: npm test
   ```

This workflow triggers on any push or pull request to the `main` branch. It runs three main steps: check out the code, set up Node.js, install dependencies, and execute tests using the self-hosted runner.

### Step 3: Testing the Pipeline

Commit and push the `.github/workflows/ci-cd-pipeline.yml` file to your GitHub repository. This will automatically trigger the defined CI job. Return to the **Actions** tab in your repository to view progress and logs.

## Troubleshooting

Running workflows on self-hosted runners can encounter several issues. Here are some common ones and their solutions:

1. **Connection Issues**: If the self-hosted runner does not show up as "Online", ensure it is running and check network/firewall settings. Consider re-running the `./config.sh` setup if necessary.

2. **Permission Errors**: Ensure your GitHub token has the appropriate permissions. Re-generate and update the token if needed.

3. **Environment Mismatches**: Verify that the required software and dependencies for the job (e.g., Node.js version) are present on your self-hosted runner.

4. **Hardware Constraints**: Ensure your runner machine meets the necessary hardware specifications for running builds/tests.

## Conclusion

Setting up GitHub Actions with self-hosted runners offers great flexibility and power over CI/CD processes. By deploying workflows on specific hardware or environments, teams can optimize performance and control beyond what is feasible with shared runners. With a reliable setup, teams can achieve seamless integration and deployment across diverse technological stacks and infrastructures.

By following this tutorial, you should be well-equipped to configure and manage self-hosted runners effectively. Remember, continuous improvement and monitoring are keys to maintaining an efficient CI/CD pipeline.

Continue to explore advanced workflow features such as matrix builds, integration with third-party services, and custom actions to further enhance your automation capabilities.
```
