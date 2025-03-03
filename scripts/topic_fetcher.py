#!/usr/bin/env python3
import requests
import json
import random
import os
import re
from datetime import datetime

class TopicFetcher:
    def __init__(self):
        self.subreddits = [
            'selfhosted',
            'homelab',
            'linux',
            'devops',
            'kubernetes',
            'docker',
            'cloudcomputing',
            'programming',
            'sysadmin',
            'techsupport',
            'windows',
            'aws',
            'azure',
            'googlecloud'
        ]
        
        # Create a list of backup topics in case API calls fail
        self.backup_topics = [
            "Setting up a home NAS with Linux",
            "Docker containers for beginners",
            "Kubernetes cluster on Raspberry Pi",
            "Automating backups for home servers",
            "Linux command line productivity tips",
            "Windows power user tricks",
            "Self-hosting your own password manager",
            "Setting up a VPN at home",
            "Cloud storage alternatives for privacy",
            "Migrating from Windows to Linux",
            "Home network security best practices",
            "Docker Compose for local development",
            "Building a home media server",
            "GitHub Actions for automated testing",
            "SSH tips and tricks for remote management",
            "Setting up a reverse proxy with Nginx",
            "Managing Docker volumes effectively",
            "CI/CD pipelines for hobbyist projects",
            "Linux server monitoring tools",
            "Setting up a smart home hub"
        ]
        
        # Patterns to check if title is in English and tech-related
        self.non_english_pattern = re.compile(r'[^\x00-\x7F]+')  # Matches non-ASCII characters
        self.tech_keywords = [
            'linux', 'windows', 'server', 'cloud', 'docker', 'kubernetes', 'k8s', 
            'devops', 'aws', 'azure', 'gcp', 'google cloud', 'api', 'code', 'coding',
            'software', 'hardware', 'network', 'security', 'hacking', 'hack', 'github',
            'git', 'development', 'programming', 'script', 'automation', 'cli', 'command',
            'terminal', 'bash', 'shell', 'python', 'javascript', 'java', 'rust', 'go',
            'database', 'sql', 'nosql', 'mongodb', 'postgresql', 'mysql', 'hosting',
            'self-hosted', 'selfhosted', 'homelab', 'home lab', 'raspberry pi', 'vm',
            'virtual machine', 'container', 'system', 'admin', 'sysadmin', 'web', 'app',
            'application', 'ci/cd', 'terraform', 'ansible', 'puppet', 'chef', 'monitor',
            'logging', 'vpn', 'router', 'firewall', 'proxy', 'nginx', 'apache', 'http',
            'https', 'ssh', 'ftp', 'dns', 'ip', 'protocol', 'framework', 'library',
            'package', 'dependency', 'microservice', 'architecture', 'design pattern',
            'rest', 'graphql', 'api', 'interface', 'frontend', 'backend', 'fullstack',
            'data', 'storage', 'cache', 'memory', 'cpu', 'gpu', 'processor', 'encryption'
        ]
    
    def is_valid_tech_topic(self, title):
        """Check if the topic is English and tech related"""
        # Skip topics with non-ASCII characters (likely non-English)
        if self.non_english_pattern.search(title):
            return False
            
        # Check if title contains any tech keywords
        title_lower = title.lower()
        return any(keyword in title_lower for keyword in self.tech_keywords)
    
    def get_reddit_topics(self, count=5):
        """Fetch trending topics from selected subreddits"""
        topics = []
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        
        try:
            # Randomly select subreddits to pull from
            selected_subreddits = random.sample(self.subreddits, min(5, len(self.subreddits)))
            
            for subreddit in selected_subreddits:
                response = requests.get(
                    f"https://www.reddit.com/r/{subreddit}/hot.json?limit=15",
                    headers=headers
                )
                
                if response.status_code == 200:
                    data = response.json()
                    posts = data.get('data', {}).get('children', [])
                    
                    for post in posts:
                        post_data = post.get('data', {})
                        title = post_data.get('title', '')
                        
                        # Apply more strict filtering
                        if (title and 
                            not title.lower().startswith(('[meta]', '[announcement]')) and
                            self.is_valid_tech_topic(title)):
                            
                            topics.append({
                                'title': title,
                                'source': f"r/{subreddit}",
                                'url': f"https://www.reddit.com{post_data.get('permalink', '')}"
                            })
            
            # Shuffle and limit topics
            random.shuffle(topics)
            return topics[:count]
            
        except Exception as e:
            print(f"Error fetching Reddit topics: {e}")
            return []
    
    def get_hacker_news_topics(self, count=3):
        """Fetch trending tech topics from Hacker News"""
        topics = []
        
        try:
            # Get top stories IDs
            response = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json")
            if response.status_code == 200:
                story_ids = response.json()[:30]  # Get top 30 stories to have more to filter
                
                # Get story details
                for story_id in story_ids:
                    story_response = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json")
                    if story_response.status_code == 200:
                        story = story_response.json()
                        title = story.get('title', '')
                        
                        # Apply strict filtering
                        if (title and 
                            story.get('type') == 'story' and
                            self.is_valid_tech_topic(title)):
                            
                            topics.append({
                                'title': title,
                                'source': 'Hacker News',
                                'url': story.get('url', f"https://news.ycombinator.com/item?id={story_id}")
                            })
                
                # Shuffle and limit topics
                random.shuffle(topics)
                return topics[:count]
                
        except Exception as e:
            print(f"Error fetching Hacker News topics: {e}")
            return []
    
    def get_github_trending(self, count=2):
        """Fetch trending repositories from GitHub"""
        topics = []
        
        try:
            # Filter by specific tech topics
            tech_topics = ["python", "javascript", "devops", "kubernetes", "docker", "linux", "aws", "azure"]
            selected_topic = random.choice(tech_topics)
            
            # GitHub doesn't have an official API for trending, so we'll use a workaround
            response = requests.get(
                f"https://api.github.com/search/repositories?q=topic:{selected_topic} created:>2023-01-01&sort=stars&order=desc",
                headers={'Accept': 'application/vnd.github.v3+json'}
            )
            
            if response.status_code == 200:
                repos = response.json().get('items', [])
                
                for repo in repos:
                    name = repo.get('name', '')
                    description = repo.get('description', '')
                    
                    # Skip repos with non-English names or descriptions
                    if (name and description and 
                        not self.non_english_pattern.search(name) and 
                        not self.non_english_pattern.search(description)):
                        
                        title = f"Exploring {name}: {description}"
                        
                        if self.is_valid_tech_topic(title):
                            topics.append({
                                'title': title,
                                'source': 'GitHub Trending',
                                'url': repo['html_url']
                            })
                
                # Shuffle and limit topics
                random.shuffle(topics)
                return topics[:count]
                
        except Exception as e:
            print(f"Error fetching GitHub trending: {e}")
            return []
    
    def get_topics(self, count=10):
        """Combine topics from all sources"""
        all_topics = []
        
        # Get topics from different sources
        all_topics.extend(self.get_reddit_topics(count=6))
        all_topics.extend(self.get_hacker_news_topics(count=4))
        all_topics.extend(self.get_github_trending(count=2))
        
        # If we didn't get enough topics, add some from backup list
        if len(all_topics) < count:
            # Shuffle backup topics
            random.shuffle(self.backup_topics)
            # Add backup topics as needed
            for topic in self.backup_topics[:count-len(all_topics)]:
                all_topics.append({
                    'title': topic,
                    'source': 'Curated Topic',
                    'url': None
                })
        
        # Shuffle all topics
        random.shuffle(all_topics)
        
        # Final filtering to ensure all topics are valid
        filtered_topics = [topic for topic in all_topics if self.is_valid_tech_topic(topic['title'])]
        
        # Return limited number of topics
        return filtered_topics[:count]
    
    def save_topics(self, filepath='topics.json'):
        """Save fetched topics to a JSON file"""
        topics = self.get_topics()
        
        # Add timestamp
        data = {
            'timestamp': datetime.now().isoformat(),
            'topics': topics
        }
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Save to file
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        return topics

if __name__ == "__main__":
    fetcher = TopicFetcher()
    topics = fetcher.save_topics('data/topics.json')
    print(f"Fetched {len(topics)} topics and saved to data/topics.json")
    for i, topic in enumerate(topics):
        print(f"{i+1}. {topic['title']} (from {topic['source']})")