import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import hashlib
import re
from config import NEWS_SOURCES, FOCUS_TOPICS
from urllib.parse import urljoin

class NewsCollector:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def collect_news(self, hours_back=2):
        """
        Collect news from all sources published within the last X hours
        Returns a list of article dictionaries
        """
        all_articles = []
        cutoff_time = datetime.now() - timedelta(hours=hours_back)
        
        for source_name, source_info in NEWS_SOURCES.items():
            try:
                if 'rss' in source_info:
                    articles = self._fetch_rss(source_name, source_info, cutoff_time)
                else:
                    articles = self._scrape_website(source_name, source_info, cutoff_time)
                
                all_articles.extend(articles)
                print(f"✓ Collected {len(articles)} articles from {source_name}")
            except Exception as e:
                print(f"✗ Error collecting from {source_name}: {str(e)}")
        
        return all_articles
    
    def _fetch_rss(self, source_name, source_info, cutoff_time):
        """Fetch articles from RSS feed"""
        articles = []
        feed = feedparser.parse(source_info['rss'])
        
        for entry in feed.entries:
            # Parse publication date
            pub_date = self._parse_date(entry.get('published', ''))
            
            if pub_date and pub_date > cutoff_time:
                article = {
                    'source': source_name,
                    'title': entry.get('title', ''),
                    'link': entry.get('link', ''),
                    'description': entry.get('description', ''),
                    'published': pub_date,
                    'language': source_info['language'],
                    'id': self._generate_id(entry.get('title', '') + entry.get('link', ''))
                }
                
                # Check if article matches focus topics
                if self._matches_topics(article):
                    articles.append(article)
        
        return articles
    
    def _scrape_website(self, source_name, source_info, cutoff_time):
        """Scrape articles directly from website (fallback for sites without RSS)"""
        articles = []
        
        try:
            response = requests.get(source_info['url'], headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Generic scraping logic - finds articles by common HTML patterns
            # This is a basic implementation; can be refined per site
            article_links = soup.find_all('a', href=True)
            
            for link in article_links[:20]:  # Limit to first 20 links
                href = link.get('href', '')
                title = link.get_text(strip=True)
                
                # Filter out navigation links, empty titles, etc.
                if len(title) > 20 and ('news' in href or 'article' in href):
                    article = {
                        'source': source_name,
                        'title': title,
                        'link': href if href.startswith('http') else source_info['url'] + href,
                        'description': '',
                        'published': datetime.now(),
                        'language': source_info['language'],
                        'id': self._generate_id(title + href)
                    }
                    
                    if self._matches_topics(article):
                        articles.append(article)
        
        except Exception as e:
            print(f"Scraping error for {source_name}: {str(e)}")
        
        return articles
    
    def _parse_date(self, date_string):
        """Parse various date formats"""
        try:
            # Try common date formats
            from dateutil import parser
            return parser.parse(date_string)
        except:
            return datetime.now()
    
    def _generate_id(self, text):
        """Generate unique ID for article based on content"""
        return hashlib.md5(text.encode()).hexdigest()
    
    def _matches_topics(self, article):
        """Check if article matches any focus topics"""
        text = (article['title'] + ' ' + article.get('description', '')).lower()
        
        # If no focus topics set, accept all
        if not FOCUS_TOPICS:
            return True
        
        # Check if any topic keyword appears in title or description
        for topic in FOCUS_TOPICS:
            if topic.lower() in text:
                return True
        
        return False
    
    def group_similar_stories(self, articles):
        """
        Group articles that are about the same story
        Returns a list of story groups
        """
        from collections import defaultdict
        
        # Simple similarity: group by common words in title
        story_groups = defaultdict(list)
        
        for article in articles:
            # Extract main keywords from title
            keywords = self._extract_keywords(article['title'])
            key = ' '.join(sorted(keywords[:3]))  # Use top 3 keywords as group key
            
            story_groups[key].append(article)
        
        # Return only groups with multiple sources or significant single sources
        important_stories = []
        for key, group in story_groups.items():
            if len(group) >= 1:  # At least one article
                important_stories.append({
                    'articles': group,
                    'importance_score': len(group),
                    'sources': list(set([a['source'] for a in group]))
                })
        
        # Sort by importance
        important_stories.sort(key=lambda x: x['importance_score'], reverse=True)
        
        return important_stories
    
    def _extract_keywords(self, text):
        """Extract important keywords from text"""
        # Remove common words and extract meaningful terms
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                     'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'be', 'been'}
        
        words = re.findall(r'\w+', text.lower())
        keywords = [w for w in words if w not in stop_words and len(w) > 3]
        
        return keywords[:5]  # Return top 5 keywords
    
    def extract_image_from_article(self, article):
        """
        Extract the main image from a news article
        Returns image URL or None
        """
        try:
            # First, try to get image from RSS feed
            if 'media_content' in article and article.get('media_content'):
                return article['media_content'][0].get('url')
            
            # Try enclosures (some RSS feeds use this)
            if 'enclosures' in article and article.get('enclosures'):
                for enclosure in article['enclosures']:
                    if 'image' in enclosure.get('type', ''):
                        return enclosure.get('href')
            
            # If not in feed, scrape the article page
            if 'link' in article:
                return self._scrape_image_from_url(article['link'])
            
        except Exception as e:
            print(f"Image extraction error: {str(e)}")
        
        return None
    
    def _scrape_image_from_url(self, url):
        """Scrape the main image from article URL"""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Try Open Graph image (most reliable)
            og_image = soup.find('meta', property='og:image')
            if og_image and og_image.get('content'):
                return og_image['content']
            
            # Try Twitter card image
            twitter_image = soup.find('meta', attrs={'name': 'twitter:image'})
            if twitter_image and twitter_image.get('content'):
                return twitter_image['content']
            
            # Try to find main article image
            # Look for images in article content
            article_tag = soup.find('article') or soup.find('div', class_=re.compile(r'article|content|post'))
            if article_tag:
                img = article_tag.find('img')
                if img and img.get('src'):
                    img_url = img['src']
                    # Convert relative URL to absolute
                    if not img_url.startswith('http'):
                        img_url = urljoin(url, img_url)
                    return img_url
            
            # Last resort: first image on page with reasonable size
            for img in soup.find_all('img'):
                src = img.get('src', '')
                # Skip small images (likely icons, logos)
                width = img.get('width', '0')
                if src and (not width or int(width.replace('px', '').strip()) if width.isdigit() else 999) > 200:
                    if not src.startswith('http'):
                        src = urljoin(url, src)
                    return src
            
        except Exception as e:
            print(f"URL scraping error for {url}: {str(e)}")
        
        return None
    
    def download_image(self, image_url, save_path):
        """Download image from URL and save locally"""
        try:
            response = requests.get(image_url, headers=self.headers, timeout=15)
            if response.status_code == 200:
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                return True
        except Exception as e:
            print(f"Image download error: {str(e)}")
        return False

# Quick test function
if __name__ == "__main__":
    collector = NewsCollector()
    articles = collector.collect_news(hours_back=24)
    print(f"\n📰 Total articles collected: {len(articles)}")
    
    stories = collector.group_similar_stories(articles)
    print(f"📊 Important stories found: {len(stories)}")
    
    for i, story in enumerate(stories[:3], 1):
        print(f"\n{i}. Story covered by {story['importance_score']} source(s):")
        print(f"   Sources: {', '.join(story['sources'])}")
        print(f"   Title: {story['articles'][0]['title'][:80]}...")
