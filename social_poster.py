from instagrapi import Client
import facebook
from datetime import datetime
from config import (
    INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD,
    FACEBOOK_PAGE_ACCESS_TOKEN, FACEBOOK_PAGE_ID,
    CAPTION_TEMPLATE
)

class SocialMediaPoster:
    def __init__(self):
        self.instagram_client = None
        self.facebook_api = None
        
        # Initialize clients if credentials are provided
        if INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD:
            self._init_instagram()
        
        if FACEBOOK_PAGE_ACCESS_TOKEN and FACEBOOK_PAGE_ID:
            self._init_facebook()
    
    def _init_instagram(self):
        """Initialize Instagram client"""
        try:
            self.instagram_client = Client()
            self.instagram_client.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
            print("✓ Instagram login successful")
        except Exception as e:
            print(f"✗ Instagram login failed: {str(e)}")
            self.instagram_client = None
    
    def _init_facebook(self):
        """Initialize Facebook API"""
        try:
            self.facebook_api = facebook.GraphAPI(access_token=FACEBOOK_PAGE_ACCESS_TOKEN)
            print("✓ Facebook API initialized")
        except Exception as e:
            print(f"✗ Facebook API initialization failed: {str(e)}")
            self.facebook_api = None
    
    def post_to_all(self, processed_story, image_paths):
        """
        Post to all configured platforms
        image_paths should be a dict like {'instagram': 'path.png', 'facebook': 'path.png'}
        """
        results = {}
        
        # Generate caption
        caption = self._generate_caption(processed_story)
        
        # Post to Instagram
        if self.instagram_client and 'instagram' in image_paths:
            results['instagram'] = self.post_to_instagram(
                image_paths['instagram'], 
                caption
            )
        
        # Post to Facebook
        if self.facebook_api and 'facebook' in image_paths:
            results['facebook'] = self.post_to_facebook(
                image_paths['facebook'],
                caption
            )
        
        return results
    
    def post_to_instagram(self, image_path, caption):
        """Post to Instagram feed"""
        if not self.instagram_client:
            return {'success': False, 'error': 'Instagram not configured'}
        
        try:
            # Upload photo
            media = self.instagram_client.photo_upload(
                image_path,
                caption=caption
            )
            
            print(f"✓ Posted to Instagram: {media.pk}")
            return {
                'success': True,
                'post_id': media.pk,
                'url': f"https://instagram.com/p/{media.code}"
            }
        
        except Exception as e:
            print(f"✗ Instagram posting failed: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def post_to_facebook(self, image_path, caption):
        """Post to Facebook page"""
        if not self.facebook_api:
            return {'success': False, 'error': 'Facebook not configured'}
        
        try:
            # Upload photo to Facebook
            with open(image_path, 'rb') as image_file:
                response = self.facebook_api.put_photo(
                    image=image_file,
                    message=caption
                )
            
            post_id = response.get('id', '')
            print(f"✓ Posted to Facebook: {post_id}")
            
            return {
                'success': True,
                'post_id': post_id,
                'url': f"https://facebook.com/{post_id}"
            }
        
        except Exception as e:
            print(f"✗ Facebook posting failed: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def _generate_caption(self, processed_story):
        """Generate caption from template"""
        caption = CAPTION_TEMPLATE.format(
            summary=processed_story['summary'],
            sources=', '.join(processed_story['sources']),
            timestamp=datetime.now().strftime("%B %d, %Y at %I:%M %p"),
            hashtags=processed_story['hashtags']
        )
        
        # Instagram has a 2200 character limit
        if len(caption) > 2200:
            caption = caption[:2197] + "..."
        
        return caption
    
    def save_for_manual_posting(self, processed_story, image_paths):
        """
        Save caption and images for manual posting
        Useful when API credentials aren't set up yet
        """
        caption = self._generate_caption(processed_story)
        
        # Save caption to text file
        caption_file = f"{image_paths.get('instagram', image_paths.get('facebook'))}_caption.txt"
        with open(caption_file, 'w', encoding='utf-8') as f:
            f.write(caption)
        
        print(f"\n{'='*60}")
        print("📱 READY FOR MANUAL POSTING")
        print(f"{'='*60}")
        print(f"\n📸 Images:")
        for platform, path in image_paths.items():
            print(f"  {platform}: {path}")
        print(f"\n📝 Caption saved to: {caption_file}")
        print(f"\n{'='*60}\n")
        
        return {
            'caption_file': caption_file,
            'images': image_paths
        }

# Test function
if __name__ == "__main__":
    poster = SocialMediaPoster()
    
    # Test data
    test_story = {
        'summary': 'Bangladesh Cricket Team makes historic victory! 🏏',
        'sources': ['daily_star', 'bdnews24'],
        'hashtags': '#Cricket #Bangladesh #Victory'
    }
    
    # Test with dummy image paths
    test_images = {
        'instagram': 'test_instagram.png',
        'facebook': 'test_facebook.png'
    }
    
    # If no credentials, save for manual posting
    if not (INSTAGRAM_USERNAME and FACEBOOK_PAGE_ACCESS_TOKEN):
        poster.save_for_manual_posting(test_story, test_images)
    else:
        results = poster.post_to_all(test_story, test_images)
        print("Results:", results)
