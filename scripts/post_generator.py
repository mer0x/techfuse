#!/usr/bin/env python3
import os
import json
import re
import random
import time
from datetime import datetime
from openai import OpenAI
import yaml
import argparse
import glob

class PostGenerator:
    def __init__(self, api_key=None):
        # Use API key from environment variable if not provided
        self.api_key = api_key or os.environ.get('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass it as argument.")
        
        # Initialize OpenAI client
        self.client = OpenAI(api_key=self.api_key)
        
        # Set up paths
        self.content_dir = "content/posts"
        self.data_dir = "data"
        self.topics_file = os.path.join(self.data_dir, "topics.json")
        self.history_file = os.path.join(self.data_dir, "post_history.json")
        
        # Debug information
        print(f"Current working directory: {os.getcwd()}")
        print(f"Topics file path: {self.topics_file}")
        print(f"Topics file exists: {os.path.exists(self.topics_file)}")
        print(f"Content directory exists: {os.path.exists(self.content_dir)}")
        
        # Create directories if they don't exist
        os.makedirs(self.content_dir, exist_ok=True)
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Initialize post history
        self.post_history = self._load_post_history()
    
    def _load_post_history(self):
        """Load post history from file or create new history file"""
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    print(f"Error: Could not parse {self.history_file}. Creating new history.")
                    return {'posts': []}
        return {'posts': []}
    
    def _save_post_history(self):
        """Save post history to file"""
        with open(self.history_file, 'w') as f:
            json.dump(self.post_history, f, indent=2)
    
    def _load_topics(self):
        """Load topics from file"""
        if os.path.exists(self.topics_file):
            with open(self.topics_file, 'r') as f:
                try:
                    data = json.load(f)
                    return data.get('topics', [])
                except json.JSONDecodeError:
                    print(f"Error: Could not parse {self.topics_file}.")
                    return []
        else:
            print(f"Topics file not found at {self.topics_file}")
            print(f"Directory contents of {self.data_dir}: {os.listdir(self.data_dir) if os.path.exists(self.data_dir) else 'directory does not exist'}")
            return []
    
    def _slugify(self, title):
        """Convert title to URL-friendly slug"""
        # Convert to lowercase and replace spaces with hyphens
        slug = title.lower().strip()
        # Remove special characters
        slug = re.sub(r'[^\w\s-]', '', slug)
        # Replace whitespace with single dash
        slug = re.sub(r'[\s_-]+', '-', slug)
        # Remove leading/trailing dashes
        slug = slug.strip('-')
        return slug
    
    def _extract_title_from_content(self, content):
        """Extract title from generated content"""
        # Look for title in the markdown content
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if title_match:
            return title_match.group(1).strip()
        
        # If no title found, use the first line
        first_line = content.strip().split('\n')[0]
        return first_line[:60].strip()  # Limit to 60 chars
    
    def _is_title_duplicate(self, title):
        """Check if title has been used before"""
        # Check against post history
        for post in self.post_history['posts']:
            if post['title'].lower() == title.lower():
                return True
        
        # Check existing files
        existing_posts = glob.glob(f"{self.content_dir}/*.md")
        for post_file in existing_posts:
            try:
                with open(post_file, 'r') as f:
                    content = f.read()
                    frontmatter_match = re.search(r'^---\n(.+?)\n---', content, re.DOTALL)
                    if frontmatter_match:
                        frontmatter = yaml.safe_load(frontmatter_match.group(1))
                        if frontmatter.get('title', '').lower() == title.lower():
                            return True
            except:
                continue
        
        return False
    
    def _clean_tag(self, tag):
        """Clean a tag from special characters and formatting"""
        # Remove markdown formatting (**, *, __, _, etc.)
        clean = re.sub(r'[\*\_\`\#\~\^\[\]\(\)\{\}\|\:\<\>]', '', tag)
        # Remove any other special characters
        clean = re.sub(r'[^\w\s-]', '', clean)
        # Trim whitespace
        clean = clean.strip()
        return clean
    
    def generate_post(self, topic):
        """Generate a blog post using GPT-4 Turbo"""
        source_info = f" (inspired by {topic['source']})" if topic.get('source') else ""
        reference_url = topic.get('url', '')
        
        prompt = f"""
You are writing a technical blog post about: "{topic['title']}"{source_info}.

Write a comprehensive, clear, and concise technical tutorial or guide in English. The post should:
1. Be titled with a clear, SEO-friendly headline (use a # heading)
2. Include a brief introduction that explains why this topic matters
3. Provide step-by-step instructions when applicable
4. Include relevant code examples with explanations when appropriate
5. Be technically accurate and up-to-date
6. End with a conclusion summarizing key takeaways
7. Use markdown formatting throughout

The content should be informative but not overly long (800-1200 words). It should be helpful for both beginners and more technical users.
Include 2-5 relevant tags that describe the post's content. Write them as a simple comma-separated list without any formatting like bold (**) or italics (*).

Reference URL (if you need inspiration, but don't cite directly): {reference_url}
"""
        
        try:
            # Using the new OpenAI API format
            response = self.client.chat.completions.create(
                model="gpt-4.5-preview",  # Updated model name
                messages=[
                    {"role": "system", "content": "You are an expert technical writer who creates clear, concise, and accurate blog posts about IT topics."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=3000
            )
            
            content = response.choices[0].message.content.strip()
            
            # Extract title
            title = self._extract_title_from_content(content)
            
            # Check for duplicate title
            if self._is_title_duplicate(title):
                # If duplicate, try to generate a new title
                title_prompt = f"The title '{title}' has already been used. Please generate a new, unique title for this blog post about {topic['title']} that is different but still SEO-friendly."
                
                # Using the new OpenAI API format
                title_response = self.client.chat.completions.create(
                    model="gpt-4.5-preview",  # Updated model name
                    messages=[
                        {"role": "system", "content": "You are an expert at creating SEO-friendly, unique blog post titles."},
                        {"role": "user", "content": title_prompt}
                    ],
                    temperature=0.8,
                    max_tokens=100
                )
                
                new_title = title_response.choices[0].message.content.strip()
                # Remove quotes if present
                new_title = new_title.strip('"\'')
                # Remove markdown heading syntax if present
                new_title = re.sub(r'^#\s+', '', new_title)
                
                # Update the content with the new title
                content = re.sub(r'^#\s+.+$', f"# {new_title}", content, count=1, flags=re.MULTILINE)
                title = new_title
            
            # Extract tags from content
            tags = []
            tags_match = re.search(r'Tags:?\s*(.+?)$', content, re.MULTILINE | re.IGNORECASE)
            if tags_match:
                tags_str = tags_match.group(1)
                # Remove the tags line from content
                content = re.sub(r'Tags:?\s*.+?$', '', content, flags=re.MULTILINE | re.IGNORECASE)
                
                # Parse tags and clean them
                if ',' in tags_str:
                    tags = [self._clean_tag(tag) for tag in tags_str.split(',') if self._clean_tag(tag)]
                elif ' ' in tags_str:
                    tags = [self._clean_tag(tag) for tag in tags_str.split() if self._clean_tag(tag)]
            
            # If no tags were found, generate some
            if not tags:
                topic_words = topic['title'].lower().split()
                possible_tags = ['linux', 'windows', 'docker', 'kubernetes', 'cloud', 
                                'tutorial', 'guide', 'server', 'devops', 'homelab', 
                                'selfhosted', 'security', 'networking', 'automation']
                
                # Add topic-specific tags
                for word in topic_words:
                    if word in possible_tags and word not in tags:
                        tags.append(word)
                
                # Add a few random relevant tags if needed
                while len(tags) < 3:
                    tag = random.choice(possible_tags)
                    if tag not in tags:
                        tags.append(tag)
            
            return {
                'title': title,
                'content': content,
                'tags': tags,
                'topic': topic['title'],
                'source': topic.get('source', 'Generated Topic'),
                'reference_url': reference_url
            }
            
        except Exception as e:
            print(f"Error generating post: {e}")
            return None
    
    def create_post_file(self, post_data):
        """Create a markdown file for the post with frontmatter"""
        try:
            title = post_data['title']
            content = post_data['content']
            tags = post_data['tags']
            
            # Create slug from title
            slug = self._slugify(title)
            
            # Get current date
            date = datetime.now().strftime('%Y-%m-%d')
            
            # Create frontmatter
            frontmatter = {
                'title': title,
                'date': date,
                'tags': [tag.strip() for tag in tags if tag.strip()],  # Ensure clean tags
                'description': f"A guide on {post_data['topic']}",
                'author': "Auto Blog Generator",
                'showToc': True,
                'TocOpen': False,
                'draft': False,
                'hidemeta': False,
                'comments': True,
                'disableShare': False,
                'disableHLJS': False,
                'hideSummary': False,
                'searchHidden': False,
                'ShowReadingTime': True,
                'ShowBreadCrumbs': True,
                'ShowPostNavLinks': True,
                'ShowWordCount': True,
                'ShowRssButtonInSectionTermList': True,
                'UseHugoToc': True
            }
            
            # Convert frontmatter to YAML
            frontmatter_yaml = yaml.dump(frontmatter, default_flow_style=False)

            # Remove the first heading (title) from the content since it's already in the frontmatter
            content = re.sub(r'^#\s+.+$', '', content, count=1, flags=re.MULTILINE)
            content = content.strip()

            # Create the complete post content
            full_content = f"---\n{frontmatter_yaml}---\n\n{content}"
            
            # Generate file path
            file_path = os.path.join(self.content_dir, f"{slug}.md")
            
            print(f"Writing post to {file_path}")
            
            # Write to file
            with open(file_path, 'w') as f:
                f.write(full_content)
            
            # Add to post history
            self.post_history['posts'].append({
                'title': title,
                'slug': slug,
                'date': date,
                'topic': post_data['topic'],
                'source': post_data['source'],
                'file_path': file_path
            })
            
            # Save updated history
            self._save_post_history()
            
            return file_path
            
        except Exception as e:
            print(f"Error creating post file: {e}")
            return None
    
    def generate_new_post(self):
        """Generate a new post from available topics"""
        # Load topics
        topics = self._load_topics()
        
        if not topics:
            print("No topics available. Please fetch topics first.")
            return None
        
        # Select a random topic
        topic = random.choice(topics)
        
        print(f"Generating post for topic: {topic['title']}")
        
        # Generate post
        post_data = self.generate_post(topic)
        
        if post_data:
            # Create post file
            file_path = self.create_post_file(post_data)
            
            if file_path:
                print(f"Post created: {file_path}")
                return file_path
        
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate a blog post using GPT-4 Turbo')
    parser.add_argument('--api-key', help='OpenAI API key (if not provided, will use OPENAI_API_KEY environment variable)')
    args = parser.parse_args()
    
    generator = PostGenerator(api_key=args.api_key)
    generator.generate_new_post()
