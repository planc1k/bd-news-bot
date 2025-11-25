import os
from dotenv import load_dotenv

load_dotenv()

# =============================================================================
# API KEYS - Set these in .env file or environment variables
# =============================================================================
GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')
INSTAGRAM_USERNAME = os.getenv('INSTAGRAM_USERNAME', '')
INSTAGRAM_PASSWORD = os.getenv('INSTAGRAM_PASSWORD', '')
FACEBOOK_PAGE_ACCESS_TOKEN = os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN', '')
FACEBOOK_PAGE_ID = os.getenv('FACEBOOK_PAGE_ID', '')

# =============================================================================
# NEWS SOURCES - Bangladeshi news sites
# =============================================================================
NEWS_SOURCES = {
    'prothom_alo': {
        'rss': 'https://www.prothomalo.com/feed/',
        'url': 'https://www.prothomalo.com',
        'language': 'bengali'
    },
    'daily_star': {
        'rss': 'https://www.thedailystar.net/rss.xml',
        'url': 'https://www.thedailystar.net',
        'language': 'english'
    },
    'bdnews24': {
        'rss': 'https://bdnews24.com/?widgetName=rssfeed&widgetId=1009&getXmlFeed=true',
        'url': 'https://bdnews24.com',
        'language': 'english'
    },
    'dhaka_tribune': {
        'rss': 'https://www.dhakatribune.com/feed',
        'url': 'https://www.dhakatribune.com',
        'language': 'english'
    },
    'risingbd': {
        'url': 'https://www.risingbd.com',
        'language': 'bengali'
    }
}

# =============================================================================
# CONTENT SETTINGS
# =============================================================================
# Topics to focus on (keywords for filtering)
FOCUS_TOPICS = [
    'breaking', 'latest', 'trending', 'viral',
    'politics', 'economy', 'technology', 'entertainment',
    'sports', 'cricket', 'bollywood', 'music',
    'celebrity', 'film', 'drama', 'culture'
]

# Minimum number of sources covering same story to consider it "important"
MIN_SOURCES_FOR_IMPORTANCE = 2

# Maximum posts per day
MAX_POSTS_PER_DAY = 20

# Check interval in minutes
CHECK_INTERVAL_MINUTES = 10

# Language preference: 'english', 'bengali', or 'both'
POST_LANGUAGE = 'english'

# =============================================================================
# IMAGE DESIGN SETTINGS
# =============================================================================
IMAGE_SETTINGS = {
    'instagram': {
        'width': 1080,
        'height': 1080
    },
    'facebook': {
        'width': 1200,
        'height': 630
    }
}

# Scroll Up Today Brand Colors
DESIGN_COLORS = {
    'primary': '#FF4444',      # Bright red (for highlights)
    'secondary': '#FF6B35',    # Orange-red (brand color)
    'accent': '#FFA500',       # Orange (sunrise logo color)
    'dark': '#000000',         # Pure black
    'text': '#FFFFFF',         # White
    'highlight_bg': '#FF4444', # Red highlight boxes
    'background_white': (255, 255, 255),  # White background option
    'background_black': (0, 0, 0),         # Black background option
    'background_gradient': [
        (0, 0, 0),             # Black
        (20, 20, 20)           # Very dark gray
    ]
}

# Brand Name
BRAND_NAME = "ScrollUp Today"
BRAND_LOGO_TEXT = "ScrollUp\nToday"  # Two-line format

# =============================================================================
# LOGO SETTINGS
# =============================================================================
# Path to your logo file (PNG with transparent background recommended)
LOGO_PATH = 'assets/scrollup_logo.png'

# Logo size (will be resized proportionally)
LOGO_WIDTH = 150  # pixels (adjust based on your logo)

# Logo position: 'bottom-right', 'bottom-left', 'top-right', 'top-left'
LOGO_POSITION = 'bottom-right'

# Add text alongside logo? True = "ScrollUp Today" text + logo, False = logo only
SHOW_BRAND_TEXT = True

# Font settings (will use PIL default fonts, but you can add custom fonts later)
FONT_SIZES = {
    'headline': 72,
    'subtext': 36,
    'source': 24
}

# =============================================================================
# SOCIAL MEDIA SETTINGS
# =============================================================================
# Caption template - ScrollUp Today style
CAPTION_TEMPLATE = """{summary}

📰 Source: {sources}
🕐 {timestamp}

{hashtags}

Follow @scrl.up for latest Bangladesh news updates 🇧🇩

#ScrollUpToday #BangladeshNews #Bangladesh #BreakingNews #LatestNews"""

# Default hashtags for different categories
CATEGORY_HASHTAGS = {
    'politics': '#Politics #Government #Bangladesh',
    'entertainment': '#Entertainment #Bollywood #PopCulture #Celebrity',
    'sports': '#Sports #Cricket #BangladeshCricket',
    'technology': '#Tech #Technology #Innovation',
    'economy': '#Business #Economy #Finance',
    'general': '#News #LatestNews #BreakingNews'
}

# =============================================================================
# STORAGE
# =============================================================================
# File to track posted stories (prevent duplicates)
POSTED_STORIES_FILE = 'posted_stories.json'

# Directory to save generated images
OUTPUT_DIR = 'generated_posts'
