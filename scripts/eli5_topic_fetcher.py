#!/usr/bin/env python3
import requests
import json
import random
import os
import re
from datetime import datetime

class ELI5TopicFetcher:
    def __init__(self):
        self.subreddits = [
            'explainlikeimfive',
            'askscience',
            'todayilearned',
            'science',
            'AskHistorians',
            'space',
            'psychology',
            'medicine',
            'biology',
            'physics',
            'chemistry',
            'history',
            'economics',
            'philosophy',
            'neuroscience'
        ]
        
        # Create a list of backup topics in case API calls fail
        self.backup_topics = [
            "Why is the sky blue?",
            "How do airplanes stay in the air?",
            "Why do we dream when we sleep?",
            "How does the internet work?",
            "What causes earthquakes and volcanoes?",
            "How do vaccines protect us from diseases?",
            "Why do leaves change colors in autumn?",
            "How does our brain store memories?",
            "Why is the ocean salty?",
            "How do bees make honey?",
            "What makes thunder and lightning happen?",
            "How do plants grow from seeds?",
            "Why do we have different seasons?",
            "How does a car engine work?",
            "What makes a rainbow appear in the sky?",
            "How do smartphones know where we are?",
            "Why do we need to sleep?",
            "How does money work in our society?",
            "What happens when we digest food?",
            "How do magnets work?"
        ]
        
        # Patterns to check if title is in English and suitable for ELI5
        self.non_english_pattern = re.compile(r'[^\x00-\x7F]+')  # Matches non-ASCII characters
        self.eli5_keywords = [
            'why', 'how', 'what', 'when', 'where', 'who', 
            'explain', 'understand', 'work', 'happen', 'cause', 'reason',
            'science', 'history', 'human', 'world', 'universe', 'earth', 'space',
            'body', 'brain', 'mind', 'heart', 'health', 'disease', 'medicine',
            'animal', 'plant', 'nature', 'environment', 'climate', 'weather',
            'technology', 'computer', 'internet', 'digital', 'social',
            'economy', 'money', 'market', 'business', 'government', 'politics',
            'culture', 'art', 'music', 'language', 'communication',
            'physics', 'chemistry', 'biology', 'psychology', 'math', 'mathematics',
            'quantum', 'cell', 'gene', 'evolution', 'energy', 'force', 'gravity'
        ]
    
    def is_valid_eli5_topic(self, title):
        """Check if the topic is English and suitable for ELI5 explanation"""
        # Skip topics with non-ASCII characters (likely non-English)
        if self.non_english_pattern.search(title):
            return False
            
        # Exclude topics that are too short
        if len(title.split()) < 3:
            return False
            
        # Check if title contains any ELI5-suitable keywords
        title_lower = title.lower()
        
        # Check if title is structured as a question or explanation request
        is_question_format = ('?' in title or 
                             title_lower.startswith(('why', 'how', 'what', 'when', 'where', 'who', 'explain')) or
                             'explain' in title_lower)
        
        # Check if title contains suitable topic keywords
        has_keywords = any(keyword in title_lower for keyword in self.eli5_keywords)
        
        return is_question_format and has_keywords
    
    def get_reddit_topics(self, count=5):
        """Fetch interesting topics from selected subreddits"""
        topics = []
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        
        try:
            # Randomly select subreddits to pull from
            selected_subreddits = random.sample(self.subreddits, min(5, len(self.subreddits)))
            
            for subreddit in selected_subreddits:
                response = requests.get(
                    f"https://www.reddit.com/r/{subreddit}/hot.json?limit=20",
                    headers=headers
                )
                
                if response.status_code == 200:
                    data = response.json()
                    posts = data.get('data', {}).get('children', [])
                    
                    for post in posts:
                        post_data = post.get('data', {})
                        title = post_data.get('title', '')
                        
                        # Apply filtering
                        if (title and 
                            self.is_valid_eli5_topic(title)):
                            
                            # Clean up title if it starts with "ELI5:" or similar
                            cleaned_title = re.sub(r'^(ELI5|eli5|Eli5|ELIF|Explain like I\'m five|TIL)[\s:]*', '', title).strip()
                            if not cleaned_title:
                                cleaned_title = title
                                
                            topics.append({
                                'title': cleaned_title,
                                'source': f"r/{subreddit}",
                                'url': f"https://www.reddit.com{post_data.get('permalink', '')}"
                            })
            
            # Shuffle and limit topics
            random.shuffle(topics)
            return topics[:count]
            
        except Exception as e:
            print(f"Error fetching Reddit topics: {e}")
            return []
    
    def get_science_daily_topics(self, count=3):
        """Fetch interesting science topics from Science Daily RSS feed"""
        topics = []
        
        try:
            # Use a parser library for RSS feeds
            response = requests.get("https://www.sciencedaily.com/rss/all.xml")
            if response.status_code == 200:
                # Extract titles from the RSS XML (simple approach)
                content = response.text
                title_matches = re.findall(r'<title><!\[CDATA\[(.*?)\]\]></title>', content)
                
                # Skip the first one as it's usually the feed title
                title_matches = title_matches[1:20] if len(title_matches) > 1 else []
                
                for title in title_matches:
                    # Convert to question format for ELI5
                    if title and not self.non_english_pattern.search(title):
                        # Get just the main subject of the headline
                        simplified = re.sub(r', study (suggests|finds|shows|reveals|reports).*$', '', title)
                        simplified = re.sub(r'\s*\(.*?\)\s*', ' ', simplified)
                        
                        # Convert to question format
                        if not simplified.endswith('?'):
                            # Randomly choose a question format
                            question_formats = [
                                f"How does {simplified} work?",
                                f"Why does {simplified} happen?",
                                f"What causes {simplified}?",
                                f"Can you explain {simplified} simply?"
                            ]
                            question = random.choice(question_formats)
                        else:
                            question = simplified
                            
                        topics.append({
                            'title': question,
                            'source': 'Science Daily',
                            'url': None  # We don't have the specific URL from this simple parsing
                        })
                
                # Shuffle and limit topics
                random.shuffle(topics)
                return topics[:count]
                
        except Exception as e:
            print(f"Error fetching Science Daily topics: {e}")
            return []
    
    def get_wikipedia_featured(self, count=2):
        """Fetch featured articles from Wikipedia and convert to ELI5 topics"""
        topics = []
        
        try:
            # Get Wikipedia's featured article
            response = requests.get("https://en.wikipedia.org/wiki/Special:RandomInCategory/Featured_articles")
            if response.status_code == 200:
                # Extract the title from the HTML
                title_match = re.search(r'<title>(.*?) - Wikipedia</title>', response.text)
                
                if title_match:
                    article_title = title_match.group(1).strip()
                    
                    # Skip items with non-English characters
                    if not self.non_english_pattern.search(article_title):
                        # Create ELI5 questions based on the article title
                        question_formats = [
                            f"What is {article_title} and why is it important?",
                            f"How would you explain {article_title} to a child?",
                            f"Why should I know about {article_title}?",
                            f"What's the simplest explanation of {article_title}?"
                        ]
                        
                        # Get the current URL after redirection
                        article_url = response.url
                        
                        for i in range(min(count, len(question_formats))):
                            topics.append({
                                'title': question_formats[i],
                                'source': 'Wikipedia Featured',
                                'url': article_url
                            })
                
                return topics[:count]
                
        except Exception as e:
            print(f"Error fetching Wikipedia topics: {e}")
            return []
    
    def get_topics(self, count=10):
        """Combine topics from all sources"""
        all_topics = []
        
        # Get topics from different sources
        all_topics.extend(self.get_reddit_topics(count=6))
        all_topics.extend(self.get_science_daily_topics(count=3))
        all_topics.extend(self.get_wikipedia_featured(count=2))
        
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
        filtered_topics = [topic for topic in all_topics if self.is_valid_eli5_topic(topic['title'])]
        
        # If still not enough topics after filtering, add more backup topics
        if len(filtered_topics) < count:
            remaining_backup = [t for t in self.backup_topics if not any(t == topic['title'] for topic in filtered_topics)]
            random.shuffle(remaining_backup)
            for topic in remaining_backup[:count-len(filtered_topics)]:
                filtered_topics.append({
                    'title': topic,
                    'source': 'Curated Topic',
                    'url': None
                })
        
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
    fetcher = ELI5TopicFetcher()
    topics = fetcher.save_topics('data/topics.json')
    print(f"Fetched {len(topics)} topics and saved to data/topics.json")
    for i, topic in enumerate(topics):
        print(f"{i+1}. {topic['title']} (from {topic['source']})")