import openai
import datetime
import os
import random
import re
import logging
from slugify import slugify

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
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
    "self-hosted VPN with OpenVPN",
    "homelab automation with Ansible",
    "compare Proxmox and ESXi for home servers",
    "setup a private cloud with Nextcloud",
    "self-host Git repositories with Gitea",
    "self-host Git repositories with GitLab",
    "monitor your infrastructure with Prometheus and Grafana",
    "self-host an email server with Mailcow",
    "block ads network-wide with Pi-hole",
    "self-host a password manager with Vaultwarden",
    "set up a Matrix server for secure communication",
    "deploy Kubernetes on bare-metal servers",
    "automate your home with Home Assistant",
    "create a media server with Plex",
    "create a media server with Jellyfin",
    "implement automated backups with BorgBackup",
    "self-host a blog with Hugo and GitHub Pages",
    "run AI models locally with Ollama",
    "secure your homelab with fail2ban",
    "containerize applications with Docker Compose",
    "implement reverse proxy with Traefik",
    "set up TrueNAS for home storage",
    "create a personal dashboard with Dashy",
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
        os.makedirs(POSTS_DIR)
        logger.info(f"Created posts directory at {POSTS_DIR}")
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
    logger.info(f"Found {len(existing_titles)} existing articles")

    attempts = 0
    while attempts < 10:  # Limit attempts to prevent infinite loops
        base_topic = random.choice(KEYWORDS)
        topic = f"How to {base_topic}"
        
        if not any(existing.lower() == topic.lower() for existing in existing_titles):
            logger.info(f"Selected new topic: {topic}")
            return topic
        
        attempts += 1
    
    # If we couldn't find a unique topic, create a more specific one
    base_topic = random.choice(KEYWORDS)
    current_date = datetime.datetime.now().strftime("%Y")
    topic = f"How to {base_topic} in {current_date}: A Complete Guide"
    logger.info(f"Selected fallback topic: {topic}")
    return topic

def generate_article(topic):
    """Generate an article using GPT-4o with research beforehand"""
    logger.info(f"Generating article for: {topic}")
    
    # Extract the core topic for better tag generation
    core_topic = topic.replace("How to ", "").lower()
    
    prompt = f"""
    You are a DevOps and self-hosting expert writing for a technical blog. 
    Your task is to write a **detailed technical tutorial** for: "{topic}".

    IMPORTANT REQUIREMENTS:
    1. The tutorial must be **at least 1500 words** and thoroughly cover the topic
    2. Include **real-world tested code examples** (Docker, Ansible, bash scripts, etc.)
    3. Use proper Hugo markdown frontmatter with these fields:
       - title: "{topic}"
       - date: [will be added automatically]
       - draft: false
       - toc: true
       - tags: [generate 5-7 relevant tags]
       - categories: [select 1-2 relevant categories]
       - summary: [write an engaging 1-2 sentence summary]
       - cover:
           image: "img/covers/{slugify(core_topic)}.jpg"
           alt: "{topic}"

    4. Structure your article with these sections:
       - Introduction (explain the value proposition)
       - Prerequisites (be specific about required hardware/software)
       - Step-by-Step Implementation (with clear code blocks)
       - Configuration and Customization
       - Security Considerations
       - Troubleshooting Common Issues
       - Conclusion and Next Steps

    5. Technical details:
       - Use markdown code blocks with proper language syntax highlighting
       - Include commented code explanations
       - For configuration files, show complete examples
       - Provide expected output where appropriate
       - Explain any environment-specific adjustments readers might need to make

    First, research why self-hosting {core_topic} is important and what the best current tools and approaches are. Then generate a comprehensive tutorial that would genuinely help a technical reader implement this solution.
    """

    client = openai.OpenAI(api_key=OPENAI_API_KEY)

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=4096,
            temperature=0.7,
        )
        
        content = response.choices[0].message.content
        logger.info(f"Generated article with {len(content.split())} words")
        return content
    except Exception as e:
        logger.error(f"Error generating article: {e}")
        raise

def extract_frontmatter_tags(content):
    """Extract tags from the generated content for tag management"""
    tags_match = re.search(r'tags:\s*\[(.*?)\]', content, re.DOTALL)
    if tags_match:
        tags_str = tags_match.group(1)
        # Clean up the tags
        tags = [tag.strip().strip('"\'') for tag in tags_str.split(',')]
        return [tag for tag in tags if tag]
    return []

def update_tags_file(new_tags):
    """Update the site's tags.yaml file with any new tags"""
    if not os.path.exists(os.path.dirname(TAGS_FILE)):
        os.makedirs(os.path.dirname(TAGS_FILE))
    
    existing_tags = []
    if os.path.exists(TAGS_FILE):
        with open(TAGS_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
            tag_matches = re.findall(r'- name: "(.*?)"', content)
            existing_tags = [tag.lower() for tag in tag_matches]
    
    new_tag_entries = []
    for tag in new_tags:
        if tag.lower() not in existing_tags:
            new_tag_entries.append(f'- name: "{tag}"\n  description: "Articles related to {tag}"\n')
    
    if new_tag_entries:
        with open(TAGS_FILE, 'a', encoding='utf-8') as f:
            f.write('\n' + '\n'.join(new_tag_entries))
        logger.info(f"Added {len(new_tag_entries)} new tags to tags.yaml")

def save_article(topic, content):
    """Save the generated article with proper Hugo frontmatter"""
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    slug = slugify(topic)
    post_path = os.path.join(POSTS_DIR, f"{date_str}-{slug}.md")
    
    # Make sure frontmatter date matches filename date
    content = re.sub(r'date:\s*["\']?.*?["\']?(\s|\n)', f'date: "{date_str}"\n', content)
    
    # Add draft: false if missing
    if "draft:" not in content:
        content = re.sub(r'---\s*\n', '---\ndraft: false\n', content)
    
    # Make sure we have proper frontmatter closure
    if not re.search(r'---\s*\n.*?\n---', content, re.DOTALL):
        content = re.sub(r'---\s*\n', '---\n', content, count=1)
        content = re.sub(r'\n([^-])', r'\n---\n\1', content, count=1)
    
    with open(post_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    logger.info(f"Saved article to {post_path}")
    return post_path, content

def main():
    """Main function to run the article generation process"""
    try:
        logger.info("Starting article generation process")
        
        # Choose a unique topic
        selected_topic = choose_unique_topic()
        
        # Generate the article
        article_content = generate_article(selected_topic)
        
        # Save the article
        post_file, content = save_article(selected_topic, article_content)
        
        # Extract and update tags
        tags = extract_frontmatter_tags(content)
        if tags:
            update_tags_file(tags)
        
        logger.info(f"✅ New post published: {post_file}")
        print(f"✅ New post published: {post_file}")
        return 0
    except Exception as e:
        logger.error(f"❌ Error in article generation process: {e}")
        return 1

if __name__ == "__main__":
    exit(main())