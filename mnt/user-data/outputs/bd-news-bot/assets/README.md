# 📁 Assets Folder

## 🎨 PUT YOUR LOGO HERE

This folder contains branding assets for your news bot.

### Required Files

**Logo File:**
```
scrollup_logo.png  ← Your actual ScrollUp Today logo goes here!
```

### File Requirements

- **Format:** PNG (with transparent background recommended)
- **Size:** At least 300x300 pixels
- **Name:** Must be exactly `scrollup_logo.png`
- **Content:** Your orange sunrise burst logo

### Current Status

✅ Placeholder created: `scrollup_logo_PLACEHOLDER.png`  
⚠️ **REPLACE THIS** with your actual logo!

### How to Add Your Logo

1. Find your ScrollUp Today logo file
2. Rename it to: `scrollup_logo.png`
3. Place it in this `assets/` folder
4. Run the bot - your logo will appear!

### Logo Configuration

Adjust logo settings in `config.py`:
- `LOGO_WIDTH = 150` - Size of logo
- `LOGO_POSITION = 'bottom-right'` - Where to place it
- `SHOW_BRAND_TEXT = True` - Show text with logo

### Need Help?

See the complete guide: `../ADD_YOUR_LOGO.md`

---

**Quick Test:**
```bash
# Check if logo exists
ls -la scrollup_logo.png

# Test the bot
cd ..
python main.py
```

Your logo will appear on every generated post! 🎨
