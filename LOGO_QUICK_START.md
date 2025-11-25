# 🎯 QUICK: ADD YOUR LOGO IN 3 STEPS

## Step 1: Find the Assets Folder
```
bd-news-bot/
  └── assets/          ← Open this folder
       ├── README.md
       └── scrollup_logo_PLACEHOLDER.png
```

## Step 2: Add Your Logo
```
1. Get your ScrollUp Today logo (the orange sunrise burst)
2. Rename it to: scrollup_logo.png
3. Place it in the assets/ folder
4. Delete (or ignore) the PLACEHOLDER file
```

**Result:**
```
bd-news-bot/
  └── assets/
       ├── README.md
       └── scrollup_logo.png  ← Your logo is here!
```

## Step 3: Run the Bot
```bash
cd bd-news-bot
python main.py
```

**Your logo will now appear on EVERY post automatically!** ✨

---

## 📐 Logo Specifications

**Perfect Logo:**
- PNG with **transparent background**
- At least **300×300 pixels**
- Your orange **sunrise burst** logo
- High resolution

**File Name (MUST BE EXACT):**
```
scrollup_logo.png
```

Not: `ScrollUp_Logo.PNG` or `scrollup-logo.png` ❌

---

## ⚙️ Customize Logo (Optional)

### Change Size
Edit `config.py`:
```python
LOGO_WIDTH = 150  # Change to: 100, 120, 150, 200, etc.
```

### Change Position
Edit `config.py`:
```python
LOGO_POSITION = 'bottom-right'  # Or: 'bottom-left', 'top-right', 'top-left'
```

### Show/Hide Text
Edit `config.py`:
```python
SHOW_BRAND_TEXT = True   # Shows "ScrollUp Today" + logo
SHOW_BRAND_TEXT = False  # Shows logo only
```

---

## ✅ What You'll Get

### Before (Without Logo)
```
[Post with text branding]
ScrollUp Today ●
```

### After (With Your Logo)
```
[Post with your actual logo]
ScrollUp Today [🌅 Your Logo]
```

---

## 🎨 On Your Posts

The logo will appear:
- ✅ **Bottom right** of every post (configurable)
- ✅ **Automatic sizing** for different platforms
- ✅ **Shadow on photos** for visibility
- ✅ **No manual work** needed!

---

## 🚨 Troubleshooting

**Logo not showing?**
```bash
# Check if file exists
ls assets/scrollup_logo.png

# Check file name is exact
# Must be: scrollup_logo.png (all lowercase)
```

**Logo too big/small?**
```python
# In config.py, change:
LOGO_WIDTH = 120  # Try different numbers
```

**Logo in wrong spot?**
```python
# In config.py, change:
LOGO_POSITION = 'top-right'  # Or other position
```

---

## 📚 Full Guide

For complete instructions, see:
- **`ADD_YOUR_LOGO.md`** - Comprehensive guide
- **`assets/README.md`** - Assets folder info
- **`config.py`** - All logo settings

---

## 🎉 That's It!

1. Add `scrollup_logo.png` to `assets/` folder
2. Run `python main.py`
3. Your logo is on every post!

**No code changes needed. Just drop the file and go!** 🚀
