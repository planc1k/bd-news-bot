# 🚀 QUICK START - 5 Minutes to Your First Post

## Step 1: Get Groq API Key (2 minutes)

1. Go to https://console.groq.com
2. Sign up (free, no credit card)
3. Click "API Keys" in sidebar
4. Click "Create API Key"
5. Copy the key

## Step 2: Setup (1 minute)

```bash
# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env

# Edit .env and paste your Groq API key
nano .env
# or use any text editor
```

In `.env`, replace this line:
```
GROQ_API_KEY=your_groq_api_key_here
```

With your actual key:
```
GROQ_API_KEY=gsk_abc123...
```

Save and exit.

## Step 3: Test (1 minute)

```bash
python test_setup.py
```

You should see all tests pass ✓

## Step 4: Run Your First Cycle (1 minute)

```bash
python main.py
```

Watch it:
1. ✓ Collect news from Bangladeshi sites
2. ✓ Analyze and group stories
3. ✓ Generate AI summaries
4. ✓ Create bold graphics
5. ✓ Save to `generated_posts/` folder

## Step 5: Check Results

```bash
ls generated_posts/
```

You'll see:
- `post_YYYYMMDD_HHMMSS_instagram.png`
- `post_YYYYMMDD_HHMMSS_facebook.png`
- `post_YYYYMMDD_HHMMSS_instagram.png_caption.txt`

Open the images - they're ready to post!

## 🎉 You're Done!

### What Happened?

The bot:
- Found breaking Bangladeshi news
- Created engaging AI summaries
- Designed bold modern graphics
- Saved everything for you to post

### Post Manually (For Now)

1. Open the PNG images
2. Read the caption from the .txt file
3. Post to Instagram/Facebook yourself

### Want Automation?

When ready for automated posting:

1. **Set up Instagram** (easier):
   - Add username/password to `.env`
   - Must be Business/Creator account

2. **Set up Facebook** (more complex):
   - Create Facebook App
   - Get Page Access Token
   - Add to `.env`

See full README.md for detailed instructions.

### Deploy to Vercel (Auto-Post Every 10 Minutes)

```bash
# Install Vercel CLI
npm install -g vercel

# Login and deploy
vercel login
vercel deploy --prod

# Add your Groq API key in Vercel dashboard:
# Project → Settings → Environment Variables
```

Done! Your bot now runs automatically every 10 minutes.

## 🎯 Next Steps

- **Customize Design**: Edit colors in `config.py`
- **Change Topics**: Adjust FOCUS_TOPICS in `config.py`
- **Add Sources**: More news sites in NEWS_SOURCES
- **Adjust Frequency**: Change CHECK_INTERVAL_MINUTES

## ⚡ Pro Tips

- Run `python main.py` anytime to manually trigger
- Check `posted_stories.json` to see what's been posted
- Images are 1080x1080 (Instagram) and 1200x630 (Facebook)
- Default: Max 20 posts per day (configurable)

## 🆘 Issues?

**"No articles found"**
- Normal for first run
- Try again in a few minutes
- News sites might be slow

**"Groq API error"**
- Check your API key is correct
- Verify it's properly in .env file

**Images look weird**
- Normal on first run
- Designs improve with more content

## 📚 Full Documentation

See `README.md` for complete documentation including:
- Detailed Instagram/Facebook setup
- Vercel deployment guide
- Troubleshooting
- Advanced configuration

---

**Questions? Check README.md or run: `python test_setup.py`**
