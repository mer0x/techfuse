import openai
import datetime
import os
import random
import re
import yaml
import logging
from slugify import slugify

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    logger.error("OPENAI_API_KEY environment variable not set")
    raise EnvironmentError("OPENAI_API_KEY environment variable not set")

# Hugo Configuration
REPO_PATH = os.path.dirname(os.path.abspath(__file__)) + "/../"
POSTS_DIR = os.path.join(REPO_PATH, "content/posts")
TAGS_FILE = os.path.join(REPO_PATH, "data/tags.yaml")

# Keywords for self-hosting and IT topics
KEYWORDS = [
    "self-hosted VPN with WireGuard",
    "homelab automation with Ansible",
    "compare Proxmox and ESXi for home servers",
    "self-host Git repositories with Gitea",
    "monitor your infrastructure with Prometheus and Grafana",
    "self-host an email server with Mailcow",
    "deploy Kubernetes on bare-metal servers",
    "automate your home with Home Assistant",
    "create a media server with Plex",
    "implement automated backups with BorgBackup",
    "run AI models locally with Ollama",
    "secure your homelab with fail2ban",
    "set up TrueNAS for home storage",
]

# Categories for better organization
CATEGORIES = [
    "Infrastructure",
    "Security",
    "Networking",
    "Storage",
    "Self-Hosting",
    "Automation",
    "DevOps",
    "Containerization",
    "Monitoring",
    "Backup Solutions"
]


def get_existing_topics():
    """Check existing articles to avoid duplicates"""
    existing_titles = set()
    
    if not os.path.exists(POSTS_DIR):
        os.makedirs(POSTS_DIR, exist_ok=True)
        return existing_titles

    for filename in os.listdir(POSTS_DIR):
        if filename.endswith(".md"):
            with open(os.path.join(POSTS_DIR, filename), "r", encoding="utf-8") as f:
                content = f.read()
                title_match = re.search(r'title:\s*"([^"]+)"', content)
                if title_match:
                    existing_titles.add(title_match.group(1))
    
    return existing_titles


def choose_unique_topic():
    """Choose a new and unique topic based on keywords"""
    existing_titles = get_existing_topics()
    
    for _ in range(10):  # Limit attempts to prevent infinite loops
        base_topic = random.choice(KEYWORDS)
        topic = f"How to {base_topic}"
        
        if topic.lower() not in (title.lower() for title in existing_titles):
            return topic

    # If no unique topic found, append year
    current_date = datetime.datetime.now().strftime("%Y")
    return f"How to {random.choice(KEYWORDS)} in {current_date}: A Complete Guide"


def generate_article(topic):
    """Generate an article using GPT-4o"""
    logger.info(f"Generating article for: {topic}")
    
    prompt = f"""
    Write a technical blog post for Hugo (Papeemod theme) about "{topic}".
    Requirements:
    - Detailed, 1500+ words
    - Real-world tested code examples (Docker, Ansible, bash scripts)
    - Hugo Markdown frontmatter with:
      - title: "{topic}"
      - date: auto-generated
      - draft: false
      - toc: true
      - tags: (5-7 relevant)
      - categories: (1-2 relevant)
      - summary: short overview
      - cover:
          image: "img/covers/{slugify(topic)}.jpg"
          alt: "{topic}"
    - Sections:
      - Introduction
      - Prerequisites
      - Step-by-Step Implementation
      - Configuration and Customization
      - Security Considerations
      - Troubleshooting
      - Conclusion
    - Use Markdown syntax with proper headers and code blocks.
    """

    client = openai.OpenAI(api_key=OPENAI_API_KEY)

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=4096,
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error generating article: {e}")
        raise


def save_article(topic, content):
    """Save article with correct Hugo frontmatter"""
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    slug = slugify(topic)
    post_path = os.path.join(POSTS_DIR, f"{date_str}-{slug}.md")

    # Ensure correct frontmatter format
    frontmatter = {
        "title": topic,
        "date": date_str,
        "draft": False,
        "toc": True,
        "tags": [],
        "categories": [],
        "summary": f"A complete guide on {topic}.",
        "cover": {
            "image": f"img/covers/{slug}.jpg",
            "alt": topic
        }
    }

    content = f"---\n{yaml.dump(frontmatter, default_flow_style=False)}---\n\n" + content

    with open(post_path, "w", encoding="utf-8") as f:
        f.write(content)

    logger.info(f"Saved article to {post_path}")
    return post_path


def main():
    """Main function"""
    try:
        topic = choose_unique_topic()
        content = generate_article(topic)
        post_file = save_article(topic, content)
        logger.info(f"✅ New post published: {post_file}")
    except Exception as e:
        logger.error(f"❌ Error: {e}")


if __name__ == "__main__":
    main()