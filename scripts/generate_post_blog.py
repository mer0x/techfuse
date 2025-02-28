import openai
import datetime
import os
import random
import re
import logging
from slugify import slugify

# Configurare logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Configurare OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    logger.error("OPENAI_API_KEY environment variable not set")
    raise EnvironmentError("OPENAI_API_KEY environment variable not set")

# Configurare Hugo
REPO_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
POSTS_DIR = os.path.join(REPO_PATH, "content/posts")
TAGS_FILE = os.path.join(REPO_PATH, "data/tags.yaml")

# Lista de subiecte pentru generare
KEYWORDS = [
    "self-host a VPN with WireGuard",
    "automate homelab with Ansible",
    "compare Proxmox and ESXi for home servers",
    "setup a private cloud with Nextcloud",
    "monitor infrastructure with Prometheus and Grafana",
    "deploy Kubernetes on bare-metal servers",
    "self-host a blog with Hugo and GitHub Pages",
]

CATEGORIES = [
    "Infrastructure",
    "Security",
    "Self-Hosting",
    "Automation",
    "Containerization",
    "Monitoring",
]

def get_existing_titles():
    """Verifică articolele existente pentru a evita duplicatele"""
    existing_titles = set()
    if not os.path.exists(POSTS_DIR):
        os.makedirs(POSTS_DIR)
        return existing_titles
    
    for filename in os.listdir(POSTS_DIR):
        if filename.endswith(".md"):
            with open(os.path.join(POSTS_DIR, filename), "r", encoding="utf-8") as f:
                content = f.read()
                title_match = re.search(r'^title:\s*"([^"]+)"', content, re.MULTILINE)
                if title_match:
                    existing_titles.add(title_match.group(1).strip())
    
    return existing_titles

def choose_unique_topic():
    """Alege un topic unic din lista de keywords"""
    existing_titles = get_existing_titles()
    attempts = 0

    while attempts < 10:
        topic = f"How to {random.choice(KEYWORDS)}"
        if topic not in existing_titles:
            return topic
        attempts += 1

    return f"How to {random.choice(KEYWORDS)} - Complete Guide {datetime.datetime.now().year}"

def generate_article(topic):
    """Generează conținutul articolului folosind OpenAI"""
    logger.info(f"Generating article: {topic}")
    
    # Select appropriate tags and categories
    tags = []
    relevant_keywords = re.findall(r'\b\w+\b', topic.lower())
    for keyword in relevant_keywords:
        if keyword not in ['how', 'to', 'with', 'and', 'for', 'a']:
            tags.append(keyword.capitalize())
    
    # Choose categories
    category_choices = []
    for category in CATEGORIES:
        for keyword in relevant_keywords:
            if keyword.lower() in category.lower():
                category_choices.append(category)
                break
    
    if not category_choices and CATEGORIES:
        category_choices = [random.choice(CATEGORIES)]
    
    # Prepare prompt for OpenAI
    prompt = f"""
    Write a comprehensive technical tutorial on "{topic}".
    
    Rules:
    - The tutorial must be at least 1500 words
    - Use Markdown formatting
    - Include real, working code examples (configurations, commands, scripts)
    - Format as: Introduction, Prerequisites, Step-by-step Guide, Security Considerations, Troubleshooting, Conclusion
    - DO NOT include any frontmatter in your response
    - Start directly with the main heading: "# {topic}"
    - Be technically accurate and provide practical solutions
    """

    client = openai.OpenAI(api_key=OPENAI_API_KEY)

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=4096,
            temperature=0.7,
        )
        
        content = response.choices[0].message.content.strip()
        
        # Remove any frontmatter if it was included despite instructions
        content = re.sub(r'^---.*?---\s*', '', content, flags=re.DOTALL)
        
        # Ensure content starts with heading
        if not content.startswith("# "):
            content = f"# {topic}\n\n{content}"
            
        return content, tags, category_choices
    except Exception as e:
        logger.error(f"Error generating article: {e}")
        return None, [], []

def save_article(topic, content, tags, categories):
    """Salvează articolul cu un frontmatter corect"""
    if not os.path.exists(POSTS_DIR):
        os.makedirs(POSTS_DIR)
        
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    slug = slugify(topic)
    post_path = os.path.join(POSTS_DIR, f"{date_str}-{slug}.md")

    # Clean and limit tags and categories
    # Ensure we have at least a few tags if the auto-generation didn't work well
    if not tags:
        tags = ["Tutorial", "Technical", "Guide"]
    
    # Format tags and categories for YAML frontmatter
    tags_str = ", ".join([f'"{tag}"' for tag in tags[:5]])
    categories_str = ", ".join([f'"{cat}"' for cat in categories[:2]])

    frontmatter = f"""---
title: "{topic}"
date: {date_str}
draft: false
toc: true
tags: [{tags_str}]
categories: [{categories_str}]
summary: "A comprehensive guide on {topic}."
---

"""

    with open(post_path, "w", encoding="utf-8") as f:
        f.write(frontmatter + content)

    logger.info(f"Saved article to {post_path}")
    return post_path

def main():
    """Rulează procesul de generare și salvare"""
    try:
        topic = choose_unique_topic()
        content, tags, categories = generate_article(topic)
        if content:
            save_article(topic, content, tags, categories)
            logger.info(f"✅ New post generated: {topic}")
        else:
            logger.error("❌ Failed to generate content")
    except Exception as e:
        logger.error(f"❌ Error: {e}")

if __name__ == "__main__":
    main()