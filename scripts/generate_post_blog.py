import openai
import datetime
import os
import random

# Configurare OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Configurare Hugo
REPO_PATH = os.path.dirname(os.path.abspath(__file__)) + "/../"
POSTS_DIR = os.path.join(REPO_PATH, "content/posts")

# Listă de subiecte IT Self-Hosted
TOPICS = [
    "How to set up a self-hosted VPN with WireGuard",
    "Proxmox vs ESXi: Best Hypervisor for Homelab",
    "How to deploy Kubernetes on bare-metal servers",
    "Setting up Pi-hole for network-wide ad blocking",
    "How to monitor your servers using Prometheus and Grafana",
    "Automating server deployment with Ansible and Terraform",
    "Hosting your own cloud storage with Nextcloud",
    "Securing your network with pfSense firewall",
    "How to configure Cloudflare for self-hosted applications",
    "Using GitHub Actions for CI/CD in self-hosted environments",
    "Building a home server with Unraid vs TrueNAS",
    "Deploying AI models locally with Ollama & RunPod",
    "Self-hosting AI chatbots with GPT4All",
    "How to run a Matrix or XMPP chat server",
    "Automating backups with BorgBackup and Restic",
    "Setting up Jellyfin or Plex for media streaming",
    "How to host your own email server with Mailcow",
]

# Alegem un subiect random
selected_topic = random.choice(TOPICS)

# Generare articol folosind GPT-4o
def generate_article():
    prompt = f"""
    Write a **detailed, technical tutorial** for the topic: "{selected_topic}".
    The tutorial must:
    - Be **at least 800 words long**.
    - Contain **real-world tested code examples**.
    - Have a **structured format**: Introduction, Prerequisites, Implementation, Troubleshooting, Conclusion.
    - Be in **Markdown format** for Hugo.
    - Include a **title and relevant tags**.
    """

    client = openai.OpenAI(api_key=OPENAI_API_KEY)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=4000,
    )

    return response.choices[0].message.content

# Salvăm articolul generat în Hugo
def save_article(content):
    date_str = datetime.datetime.now().strftime("%Y-%m-%d-%H%M")
    slug = selected_topic.lower().replace(" ", "-").replace("/", "").replace(":", "")

    post_path = os.path.join(POSTS_DIR, f"{date_str}-{slug}.md")

    frontmatter = f"""---
title: "{selected_topic}"
date: {date_str}
tags: ["Self-Hosting", "DevOps", "Homelab", "Networking"]
categories: ["IT Tutorials"]
draft: false
---

"""

    with open(post_path, "w", encoding="utf-8") as f:
        f.write(frontmatter + content)

    return post_path

if __name__ == "__main__":
    article_content = generate_article()
    post_file = save_article(article_content)
    print(f"✅ New post published: {post_file}")