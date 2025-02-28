import openai
import datetime
import os
import random

# Configurare OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Configurare Hugo
REPO_PATH = os.path.dirname(os.path.abspath(__file__)) + "/../"
POSTS_DIR = os.path.join(REPO_PATH, "content/posts")

# Cuvinte-cheie pentru subiecte de self-hosting și IT
KEYWORDS = [
    "self-hosted VPN (WireGuard/OpenVPN)",
    "homelab automation with Ansible",
    "Proxmox vs ESXi",
    "self-hosted cloud with Nextcloud",
    "Git self-hosting (Gitea, GitLab)",
    "monitoring with Prometheus & Grafana",
    "self-hosting an email server (Mailcow)",
    "network-wide ad blocking with Pi-hole",
    "self-hosted password manager (Vaultwarden)",
    "hosting a Matrix server for secure chat",
    "deploying Kubernetes on bare-metal",
    "home automation with Home Assistant",
    "self-hosted media streaming (Plex, Jellyfin)",
    "automated backups with BorgBackup",
    "self-hosting a blog with Hugo & GitHub Pages",
    "running AI models locally with Ollama",
]

# Verifică articolele existente pentru a evita duplicate
def get_existing_topics():
    existing_titles = set()
    if not os.path.exists(POSTS_DIR):
        return existing_titles
    
    for filename in os.listdir(POSTS_DIR):
        if filename.endswith(".md"):
            with open(os.path.join(POSTS_DIR, filename), "r", encoding="utf-8") as f:
                first_line = f.readline().strip()
                if first_line.startswith("title:"):
                    existing_titles.add(first_line.replace("title:", "").strip().replace('"', ''))
    
    return existing_titles

# Alege un subiect nou și unic pe baza cuvintelor-cheie
def choose_unique_topic():
    existing_titles = get_existing_topics()

    while True:
        topic = f"How to {random.choice(KEYWORDS)}"
        
        if topic not in existing_titles:
            return topic

# Generare articol folosind GPT-4o cu research înainte
def generate_article(topic):
    prompt = f"""
    You are a DevOps and self-hosting expert. 
    Your task is to write a **detailed technical tutorial** for: "{topic}".

    - The tutorial must be **at least 1000 words long**.
    - Include **real-world tested code examples** (Docker, Ansible, Proxmox, Cloudflare, etc.).
    - Structure: **Introduction, Prerequisites, Step-by-Step Implementation, Troubleshooting, Conclusion**.
    - Use **Markdown format** for Hugo.
    - Optimize for SEO with headings and structured formatting.
    
    First, research why self-hosting {topic} is important and the best tools available. Then generate the tutorial.
    """

    client = openai.OpenAI(api_key=OPENAI_API_KEY)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=4096,
    )

    return response.choices[0].message.content

# Salvăm articolul generat în Hugo cu format de dată corect (FĂRĂ ORĂ, doar YYYY-MM-DD)
def save_article(topic, content):
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")  # Format compatibil Hugo

    slug = topic.lower().replace(" ", "-").replace("/", "").replace(":", "")

    post_path = os.path.join(POSTS_DIR, f"{date_str}-{slug}.md")

    frontmatter = f"""---
date: {date_str}

"""

    with open(post_path, "w", encoding="utf-8") as f:
        f.write(frontmatter + content)

    return post_path

if __name__ == "__main__":
    selected_topic = choose_unique_topic()
    article_content = generate_article(selected_topic)
    post_file = save_article(selected_topic, article_content)
    print(f"✅ New post published: {post_file}")