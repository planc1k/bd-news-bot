import json
import os
from datetime import datetime, timedelta
from news_collector import NewsCollector
from ai_processor import AIProcessor
from image_generator_scrollup import ScrollUpImageGenerator
from social_poster import SocialMediaPoster
from config import (
    MIN_SOURCES_FOR_IMPORTANCE,
    MAX_POSTS_PER_DAY,
    POSTED_STORIES_FILE
)

class NewsBot:
    def __init__(self):
        self.collector = NewsCollector()
        self.ai_processor = AIProcessor()
        self.image_generator = ScrollUpImageGenerator()
        self.social_poster = SocialMediaPoster()
        
        # Load posted stories to prevent duplicates
        self.posted_stories = self._load_posted_stories()
    
    def run(self):
        """Main workflow - collect, process, generate, and post"""
        print("\n" + "="*60)
        print("🤖 BANGLADESH NEWS BOT - Starting Run")
        print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60 + "\n")
        
        # Step 1: Collect news
        print("📰 Step 1: Collecting news...")
        articles = self.collector.collect_news(hours_back=2)
        print(f"   Found {len(articles)} articles\n")
        
        if not articles:
            print("✗ No new articles found. Exiting.")
            return
        
        # Step 2: Group similar stories
        print("📊 Step 2: Grouping similar stories...")
        stories = self.collector.group_similar_stories(articles)
        print(f"   Identified {len(stories)} unique stories\n")
        
        # Step 3: Filter important stories
        print("🎯 Step 3: Filtering important stories...")
        important_stories = [
            s for s in stories 
            if s['importance_score'] >= MIN_SOURCES_FOR_IMPORTANCE
        ]
        print(f"   {len(important_stories)} stories meet importance threshold\n")
        
        if not important_stories:
            print("✗ No important stories found. Exiting.")
            return
        
        # Step 4: Check daily post limit
        posts_today = self._count_posts_today()
        if posts_today >= MAX_POSTS_PER_DAY:
            print(f"⚠️  Daily limit reached ({posts_today}/{MAX_POSTS_PER_DAY}). Exiting.")
            return
        
        # Step 5: Process and post stories
        posted_count = 0
        for i, story in enumerate(important_stories, 1):
            if posts_today + posted_count >= MAX_POSTS_PER_DAY:
                print(f"\n⚠️  Daily limit reached. Stopping.")
                break
            
            # Check if already posted
            story_id = self._generate_story_id(story)
            if story_id in self.posted_stories:
                print(f"⏭️  Story {i}: Already posted, skipping.")
                continue
            
            print(f"\n🔄 Processing Story {i}/{len(important_stories)}:")
            print(f"   Sources: {', '.join(story['sources'])}")
            print(f"   Title: {story['articles'][0]['title'][:60]}...")
            
            try:
                # AI Processing
                print("   🤖 AI processing...")
                processed = self.ai_processor.process_story(story)
                
                # Extract image from news article
                print("   🖼️  Extracting image from article...")
                news_image_path = None
                if story['articles']:
                    image_url = self.collector.extract_image_from_article(story['articles'][0])
                    if image_url:
                        news_image_path = f"generated_posts/news_image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                        if self.collector.download_image(image_url, news_image_path):
                            print(f"   ✓ Downloaded image from article")
                        else:
                            news_image_path = None
                            print("   ⚠️  Image download failed, using gradient")
                    else:
                        print("   ⚠️  No image found in article, using gradient")
                
                # Generate images
                print("   🎨 Generating images...")
                image_paths = {}
                image_paths['instagram'] = self.image_generator.generate_post_image(
                    processed, 'instagram', news_image_path
                )
                image_paths['facebook'] = self.image_generator.generate_post_image(
                    processed, 'facebook', news_image_path
                )
                
                # Post to social media
                print("   📱 Posting to social media...")
                
                # Check if we have credentials
                has_instagram = bool(self.social_poster.instagram_client)
                has_facebook = bool(self.social_poster.facebook_api)
                
                if has_instagram or has_facebook:
                    results = self.social_poster.post_to_all(processed, image_paths)
                    
                    # Check if at least one platform succeeded
                    success = any(r.get('success', False) for r in results.values())
                    
                    if success:
                        print("   ✓ Posted successfully!")
                        posted_count += 1
                        
                        # Mark as posted
                        self._mark_as_posted(story_id, processed, image_paths, results)
                    else:
                        print("   ✗ All platforms failed")
                else:
                    # No credentials - save for manual posting
                    print("   ⚠️  No social media credentials configured")
                    manual_info = self.social_poster.save_for_manual_posting(
                        processed, image_paths
                    )
                    posted_count += 1
                    self._mark_as_posted(story_id, processed, image_paths, manual_info)
            
            except Exception as e:
                print(f"   ✗ Error processing story: {str(e)}")
                continue
        
        # Summary
        print("\n" + "="*60)
        print("✅ RUN COMPLETE")
        print(f"   Stories processed: {posted_count}")
        print(f"   Total posts today: {posts_today + posted_count}/{MAX_POSTS_PER_DAY}")
        print("="*60 + "\n")
    
    def _generate_story_id(self, story):
        """Generate unique ID for a story based on content"""
        import hashlib
        
        # Use titles from all articles in the group
        titles = [a['title'] for a in story['articles']]
        combined = '|'.join(sorted(titles))
        
        return hashlib.md5(combined.encode()).hexdigest()
    
    def _mark_as_posted(self, story_id, processed, image_paths, results):
        """Mark a story as posted to prevent duplicates"""
        self.posted_stories[story_id] = {
            'posted_at': datetime.now().isoformat(),
            'summary': processed['summary'],
            'sources': processed['sources'],
            'images': image_paths,
            'results': str(results)
        }
        
        self._save_posted_stories()
    
    def _load_posted_stories(self):
        """Load posted stories from file"""
        if os.path.exists(POSTED_STORIES_FILE):
            try:
                with open(POSTED_STORIES_FILE, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_posted_stories(self):
        """Save posted stories to file"""
        with open(POSTED_STORIES_FILE, 'w') as f:
            json.dump(self.posted_stories, f, indent=2)
    
    def _count_posts_today(self):
        """Count how many posts were made today"""
        today = datetime.now().date()
        count = 0
        
        for story_id, data in self.posted_stories.items():
            posted_date = datetime.fromisoformat(data['posted_at']).date()
            if posted_date == today:
                count += 1
        
        return count
    
    def cleanup_old_data(self, days=7):
        """Remove posted stories older than X days"""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        old_count = len(self.posted_stories)
        self.posted_stories = {
            story_id: data 
            for story_id, data in self.posted_stories.items()
            if datetime.fromisoformat(data['posted_at']) > cutoff_date
        }
        
        removed = old_count - len(self.posted_stories)
        if removed > 0:
            self._save_posted_stories()
            print(f"🗑️  Cleaned up {removed} old story records")

# Run the bot
if __name__ == "__main__":
    bot = NewsBot()
    bot.run()
    bot.cleanup_old_data(days=7)
