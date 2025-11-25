# 🤖 Bangladesh News Bot

Automated news aggregator that collects Bangladeshi news, creates bold modern graphics, and posts to Instagram & Facebook. **Now with a beautiful website and automatic image extraction!**

## 🌟 Features

- **Multi-Source News Collection**: Monitors 5+ popular Bangladeshi news sites
- **Ground News Style Intelligence**: Aggregates same story from multiple sources
- **AI-Powered Summarization**: Uses Groq (free) to create engaging summaries
- **🆕 Automatic Image Extraction**: Pulls images from news articles
- **Bold Modern Graphics**: Auto-generates eye-catching social media images with real news photos
- **Dual Platform Posting**: Posts to both Instagram and Facebook
- **🆕 Beautiful Website**: Display all your posts in a modern web interface
- **Smart Duplicate Prevention**: Never posts the same story twice
- **Automatic Scheduling**: Runs every 10 minutes checking for new breaking news
- **Daily Post Limits**: Prevents spam with configurable daily limits

## 📋 Prerequisites

### Required (Free)
- **Groq API Key** - Free, no credit card needed
  - Sign up at: https://console.groq.com
  - Get API key from dashboard

### Optional (For Automation)
- **Instagram Business/Creator Account**
  - Must link to a Facebook Page
  
- **Facebook Developer Account**
  - For posting to Facebook Page
  - Requires app review (1-2 weeks)

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Keys

Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` and add your API keys:
```
GROQ_API_KEY=your_groq_api_key_here
```

**Note**: Instagram and Facebook credentials are optional. Without them, the bot will generate images and captions that you can post manually.

### 3. Test Locally

Run a single cycle:
```bash
python main.py
```

You should see:
- News collected from Bangladeshi sites
- Stories grouped and analyzed
- Images generated in `generated_posts/` folder
- If no social media credentials: Files saved for manual posting

### 4. Deploy to Vercel (Automated)

#### Install Vercel CLI
```bash
npm install -g vercel
```

#### Login to Vercel
```bash
vercel login
```

#### Deploy
```bash
vercel deploy --prod
```

#### Add Environment Variables in Vercel

Go to your Vercel project dashboard → Settings → Environment Variables

Add these:
- `GROQ_API_KEY`
- `INSTAGRAM_USERNAME` (optional)
- `INSTAGRAM_PASSWORD` (optional)
- `FACEBOOK_PAGE_ACCESS_TOKEN` (optional)
- `FACEBOOK_PAGE_ID` (optional)

**Important**: Vercel will automatically run the bot every 10 minutes via cron!

## 🌐 Website (NEW!)

The bot now includes a beautiful Next.js website to display all your posts!

### Features
- Real-time feed of all posted news
- Stats dashboard (total posts, posts today, sources)
- Responsive design matching bot's aesthetic
- Category badges and hashtags
- Image display for each post

### Setup Website

```bash
cd website
npm install
npm run dev
```

Open http://localhost:3000

### Deploy Website

```bash
cd website
vercel deploy --prod
```

See `website/README.md` for full documentation.

## ⚙️ Configuration

Edit `config.py` to customize:

### News Sources
```python
# Add or remove news sources
NEWS_SOURCES = {
    'your_site': {
        'rss': 'https://yoursite.com/feed',
        'language': 'english'
    }
}
```

### Topics to Track
```python
FOCUS_TOPICS = [
    'politics', 'technology', 'entertainment',
    'sports', 'cricket', 'bollywood'
]
```

### Posting Schedule
```python
CHECK_INTERVAL_MINUTES = 10  # How often to check for news
MAX_POSTS_PER_DAY = 20       # Maximum posts per day
```

### Design Colors
```python
DESIGN_COLORS = {
    'primary': '#FF6B6B',      # Vibrant red
    'secondary': '#4ECDC4',    # Teal
    'accent': '#FFE66D',       # Yellow
}
```

### Language
```python
POST_LANGUAGE = 'english'  # 'english', 'bengali', or 'both'
```

## 📱 Setting Up Social Media (Optional)

### Instagram

**Requirements:**
1. Convert to Business or Creator account
2. Link to a Facebook Page

**Setup:**
- Use your regular username and password
- Bot uses unofficial API (faster setup, but violates ToS)
- For official API, see Facebook setup below

### Facebook

**Official API Setup (Recommended):**

1. **Create Facebook App**
   - Go to https://developers.facebook.com
   - Create new app → Business

2. **Add Permissions**
   - Add Instagram and Pages products
   - Request these permissions:
     - `pages_manage_posts`
     - `instagram_content_publish`

3. **Get Access Token**
   - Use Graph API Explorer
   - Generate User Token → Convert to Page Token
   - Copy Page Access Token and Page ID

4. **App Review**
   - Submit for review (takes 1-2 weeks)
   - Explain: "Automated news posting bot"

**Quick Alternative:**
- Start without Facebook API
- Manually post generated content
- Set up automation later

## 🗂️ Project Structure

```
bd-news-bot/
├── main.py              # Main orchestrator
├── news_collector.py    # Scrapes news from sources
├── ai_processor.py      # AI summarization (Groq)
├── image_generator.py   # Creates graphics (Pillow)
├── social_poster.py     # Posts to social media
├── config.py            # Configuration settings
├── requirements.txt     # Python dependencies
├── .env                 # Your API keys (not in git)
├── .env.example         # Template for API keys
├── vercel.json          # Vercel deployment config
├── api/
│   └── cron.py         # Vercel serverless function
└── generated_posts/     # Output images (created at runtime)
```

## 🔧 How It Works

```
1. Every 10 minutes (configurable):
   ↓
2. Collect news from Bangladeshi sites
   ↓
3. Group similar stories from multiple sources
   ↓
4. Filter for important/trending stories
   ↓
5. AI generates engaging summary
   ↓
6. Create bold modern graphics
   ↓
7. Post to Instagram & Facebook
   ↓
8. Track posted stories (no duplicates)
```

## 🎨 Generated Images Look Like

- **Real News Photos**: Automatically extracts images from articles
- **Bold Headlines**: Eye-catching text overlaid on news photos
- **Modern Design**: Geometric shapes and vibrant colors
- **Dark Overlay**: Ensures text readability over photos
- **Source Attribution**: Credits original news sources
- **Category Tags**: Visual badges for topic categories
- **Timestamps**: When the news was published
- **Fallback Design**: Uses gradient background if no image found
- **Optimized Sizes**: 
  - Instagram: 1080x1080 (square)
  - Facebook: 1200x630 (landscape)

### Image Extraction

The bot automatically:
1. Extracts images from news article pages
2. Downloads high-quality photos
3. Uses them as backgrounds in generated graphics
4. Applies dark overlay for text readability
5. Falls back to gradient design if no image available

## 🐛 Troubleshooting

### "No articles found"
- Check if news site RSS feeds are working
- Verify FOCUS_TOPICS match actual news content
- Try increasing hours_back in collector

### "Instagram login failed"
- Verify username/password
- Check if 2FA is enabled (need to use session file)
- Make sure account is Business/Creator type

### "Groq API error"
- Verify API key is correct
- Check Groq console for rate limits
- Free tier: 30 requests/minute

### Images look wrong
- Check font availability: `/usr/share/fonts/`
- Adjust FONT_SIZES in config.py
- Test locally before deploying

### Vercel deployment fails
- Ensure requirements.txt has all dependencies
- Check Vercel function logs
- Verify environment variables are set

## 📊 Monitoring

### Check Logs
```bash
# Local
python main.py

# Vercel
vercel logs
```

### View Posted Stories
```bash
cat posted_stories.json
```

### Generated Images
Check `generated_posts/` folder for all created images

## 🔐 Security Notes

- **Never commit `.env`** - It's in `.gitignore`
- **Instagram password**: Unofficial API uses plaintext password
- **Facebook tokens**: Expire periodically, may need refresh
- **Groq API**: Free tier has rate limits

## 🚀 Scaling Up

**To post more frequently:**
1. Change `CHECK_INTERVAL_MINUTES` to 5
2. Increase `MAX_POSTS_PER_DAY` to 50
3. Update vercel.json cron: `*/5 * * * *`

**To add more sources:**
1. Find RSS feed URL
2. Add to NEWS_SOURCES in config.py
3. Test with `python news_collector.py`

**To improve AI quality:**
1. Groq is already very good
2. Can switch to Claude API for better summaries
3. Adjust temperature in ai_processor.py

## 📝 License

MIT License - Use freely for any purpose

## 🤝 Contributing

Contributions welcome! Feel free to:
- Add more Bangladeshi news sources
- Improve image designs
- Add more social platforms
- Enhance AI prompts

## 💡 Tips

- **Start simple**: Run locally, post manually at first
- **Test thoroughly**: Check generated images before automating
- **Monitor closely**: First few days, check posts frequently
- **Adjust as needed**: Fine-tune topics, frequency, design
- **Backup data**: Keep posted_stories.json backed up

## 📞 Support

Questions? Check these files:
- `config.py` - All settings explained
- `main.py` - Main workflow logic
- `.env.example` - API key requirements

## ✅ Quick Checklist

- [ ] Installed Python packages
- [ ] Got Groq API key
- [ ] Created .env file
- [ ] Tested locally: `python main.py`
- [ ] Images look good in generated_posts/
- [ ] (Optional) Set up Instagram credentials
- [ ] (Optional) Set up Facebook API
- [ ] Deployed to Vercel
- [ ] Added environment variables in Vercel
- [ ] Verified cron job is running
- [ ] Monitoring posts for quality

---

**Ready to automate your news? Let's go! 🚀**

